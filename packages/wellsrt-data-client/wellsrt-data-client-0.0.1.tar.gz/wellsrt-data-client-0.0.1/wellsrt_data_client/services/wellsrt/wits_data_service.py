import logging
import json

from typing import Optional, Union
from datetime import datetime, timezone

from azure.kusto.data.helpers import dataframe_from_result_table

import pandas as pd

from wellsrt_data_client.commons import EnvVariables

from wellsrt_data_client.services.adx import AzAdxDataService

from enum import auto, IntEnum
from strenum import UppercaseStrEnum

class WitsDataService(AzAdxDataService):

    def __init__(self, env_vars:EnvVariables):
        AzAdxDataService.__init__(self, env_vars=env_vars)

    def query_logs_names(self, wellboreId: str)  -> Optional[pd.DataFrame]:
        """
        Get all avaliable logs names of a Wellbore in the ADX
        """

        client = self.get_kusto_client()
        db_name = self.get_database_name()

        kql_query = f"""
            let wellbore_id = '{wellboreId}';

            WitsDtimes
            | where WellboreId == wellbore_id
            | project WellId, WellName, WellboreId, WellboreName, LogName
            | distinct WellId, WellName, WellboreId, WellboreName, LogName
            ;
        """
        response = client.execute(database=db_name, query= kql_query)
        if len(response.primary_results) > 0:
            return dataframe_from_result_table(response.primary_results[0])
        else:
            return None

    def query_dtimes_range(self, wellboreId:str, logNames:Union[str | list[str]]) -> Optional[pd.DataFrame]:
        """
        Get Min and Max DTime of a Wellbore in the ADX
        """

        client = self.get_kusto_client()
        db_name = self.get_database_name()

        logs_names = []
        if isinstance(logNames,str):
            logs_names.append(logNames)
        elif isinstance(logNames,list):
            logs_names = logNames

        json_log_names = json.dumps(logs_names)

        kql_query = f"""
            let wellbore_id = '{wellboreId}';
            let log_names = dynamic({json_log_names});

            WitsDtimes
            | where WellboreId == wellbore_id and LogName in (log_names)
            | project WellboreId, LogName, Dtime
            | distinct  WellboreId, LogName, Dtime
            | summarize MinDtime = min(Dtime), MaxDtime = max(Dtime), LogCount=count() by  WellboreId,  LogName
            ;
        """
        
        response = client.execute(database=db_name, query= kql_query)
        if len(response.primary_results) > 0:
            return dataframe_from_result_table(response.primary_results[0])
        else:
            return None

    def query_dtimes_data(self, wellboreId:str, logName:str, curveNames:list[str], startTime:Optional[datetime] = None, endTime:Optional[datetime] = None, limit=50000) -> Optional[pd.DataFrame]:
        if wellboreId is None or logName is None or curveNames is None or len(curveNames) == 0:
            return None
        
        # get current start_dtime, end_dtime fromADX
        df_min_max_dtime = self.query_dtimes_range(wellboreId=wellboreId, logNames=logName)
        if df_min_max_dtime is None or len(df_min_max_dtime) == 0:
            # there is no data in ADX
            return None
        start_dtime = df_min_max_dtime.at[0, 'MinDtime']
        end_dtime = df_min_max_dtime.at[0, 'MaxDtime']

        # compare start_dtime and end_dtime with startTime and endTime in the parameters
        if startTime is not None and startTime > start_dtime:
            start_dtime = startTime

        if endTime is not None and endTime < end_dtime:
            end_dtime = endTime

        # process query data
        df_result:Optional[pd.DataFrame] = None
        
        client = self.get_kusto_client()
        db_name = self.get_database_name()

        if limit < 1:
            limit = 50000
        
        is_process_next_query = True

        while is_process_next_query:
            #print(f"Process - start_dtime: {start_dtime} - end_dtime: {end_dtime} - limit: {limit}")
            kql_dtime_query = self._build_dtimes_query(
                wellboreId=wellboreId, 
                logName=logName, 
                curveNames=curveNames,
                startDtime=start_dtime, 
                endDtime=end_dtime, 
                limit=limit
            )

            response = client.execute(db_name, kql_dtime_query)
            # we also support dataframes:
            df_query_result = dataframe_from_result_table(response.primary_results[0])
            total_query_item = len(df_query_result)
            # print(f"Process - total_query_item: {total_query_item}")

            if total_query_item > 0:
                if df_result is None:
                    df_result = df_query_result
                else:
                    if hasattr(df_result, 'concat'):
                        # process with Pandas v2.x
                        df_result = pd.concat([df_result, df_query_result])
                    elif hasattr(df_result, 'append'):
                        # process with Pandas v1.x
                        df_result = df_result.append(df_query_result)
                    else:
                        # process with Pandas v2.x
                        df_result = pd.concat([df_result, df_query_result])

            if total_query_item < limit:
                # quick - end of process
                is_process_next_query = False
                break
            else:
                # get Dtime of the last record
                start_dtime = df_query_result.at[df_query_result.index[-1],'Dtime']
                is_process_next_query = True
        
        return df_result

    def _build_dtimes_query(self, wellboreId:str, logName:str, curveNames:list[str], startDtime:datetime, endDtime:datetime, showUnits:bool=False, limit=10000) -> str:
        """
        Build KQL query WITS DTime Data
        """

        # reset default limit item
        if limit < 1:
            limit = 10000

        utc_format = '%Y-%m-%dT%H:%M:%S%z'
        str_start_dtime = startDtime.strftime(utc_format)
        str_end_dtime = endDtime.strftime(utc_format)

        project_curve_names, distinct_curve_names = self._build_wits_curve_query(curveNames=curveNames, showUnits=showUnits)
        
        return  f"""
            let wellbore_id = '{wellboreId}';
            let log_name = '{logName}';
            let start_dtime = datetime('{str_start_dtime}');
            let end_dtime = datetime('{str_end_dtime}');
            let limit_item = {limit};

            WitsDtimes
            | where WellboreId == wellbore_id and LogName == log_name
            | where Dtime between (start_dtime .. end_dtime)
            | project Dtime, {",".join(project_curve_names)}
            | distinct Dtime, {",".join(distinct_curve_names)}
            | order by Dtime asc  
            | take limit_item
            ;
            """
                    
    def _build_wits_curve_query(self, curveNames:list[str], showUnits:bool=False) -> tuple[list[str], list[str]]:
        """
        Build list of curve data and units query
        e.g:
            | project Dtime, d_az=todouble(Datas['az']), u_az=tostring(Units['az']), d_bdep=todouble(Datas["bdep"])
            | distinct Dtime, d_az, u_az, d_bdep
        Params:
            - curveNames: list of curve name of a Logs
            - showUnits: add units information to result
        Return
            Tuple with {0} is list of project_curve_names, {1} is list of distinct_curve_names
        """

        project_curve_names:list[str] = []
        distinct_curve_names:list[str] = []
        for curve_name in curveNames:
            formated_curve_name = self._format_curve_name(curveName=curve_name)
            project_curve_names.append(f"d_{formated_curve_name}=todouble(Datas['{curve_name}'])")
            distinct_curve_names.append(f"d_{formated_curve_name}")
            if showUnits:
                project_curve_names.append(f"u_{formated_curve_name}=tostring(Units['{curve_name}'])")
                distinct_curve_names.append(f"u_{formated_curve_name}")

        return (project_curve_names, distinct_curve_names)

    def _format_curve_name(self, curveName:str) -> str:
        """
        Remove all special characters from curve_name
        e.g:  from ts1-4 to ts1_4
        """
        special_characters=['@','#','$','*','&', '-', '|']
        normal_curve_name = curveName
        for c in special_characters:
            normal_curve_name = normal_curve_name.replace(c, "_")
        return normal_curve_name