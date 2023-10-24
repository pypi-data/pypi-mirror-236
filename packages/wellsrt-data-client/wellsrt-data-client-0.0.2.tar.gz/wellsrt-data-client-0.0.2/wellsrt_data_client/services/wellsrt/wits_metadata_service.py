import logging

import pandas as pd

import snowflake.snowpark as snowpark
import snowflake.snowpark.functions as snowfunc

from wellsrt_data_client.commons import EnvVariables

from wellsrt_data_client.services.snow import SnowDataService

from enum import auto, IntEnum
from strenum import UppercaseStrEnum

class WitsMetadataTableEnum(UppercaseStrEnum):
    WITS_WELL = auto()
    WITS_WELLBORE = auto()
    WITS_LOG = auto()
    WITS_LOGCURVE = auto()

class WitsMetaName(UppercaseStrEnum):
    WELL_ID = auto()
    WELL_NAME = auto()
    WELLBORE_ID = auto()
    WELLBORE_NAME = auto()
    LOG_ID = auto()
    LOG_NAME = auto()
    LOG_TYPE = auto()
    CURVE_ID = auto()
    CURVE_NAME = auto()
    UNIT = auto()
    DESCRIPTION = auto()

class WitsMetadataService(SnowDataService):
    """
     WitsMetadataService provides a common/utility methods to access to WellsRT Metadata tables
     e.g. WITS_WELL, WITS_WELLBORE, WITS_LOGS, WITS_LOGCURVE
    """
    def __init__(self, env_vars:EnvVariables):
        SnowDataService.__init__(self, env_vars=env_vars)
        
    def metadata(self, table: WitsMetadataTableEnum, col_filters: list[tuple[str, str]]) -> snowpark.DataFrame:
        """
        Get  Well Metadata in the snowflake.snowpark.DataFrame format.
        Ref: https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/dataframe
        """       
        tbl = self.session.table(name=table.name)
        # filter data
        having_filter = False

        where_filter = None
        for col_filter in col_filters:
            # col_name = col_filter[0]
            # col_value = col_filter[1]
            col_name, col_value = col_filter
            if col_name is not None and col_value is not None:
                if where_filter is None:
                    where_filter = (snowfunc.col(col_name) == col_value)
                else:
                    where_filter = where_filter & (snowfunc.col(col_name) == col_value)

        if where_filter is not None:
            return tbl.filter(where_filter)
        else:
            return tbl

    def wells(self, wellId:str = None, is_show_full=False) -> snowpark.DataFrame:
        """
        Get WITSML Well Metadata in the snowflake.snowpark.DataFrame format.
        Ref: https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/dataframe
        """
        df = self.metadata(
            table=WitsMetadataTableEnum.WITS_WELL,
            col_filters=[
                (WitsMetaName.WELL_ID, wellId)
            ]
        )
        if is_show_full:
            return df
        else:
            return df.select(
                WitsMetaName.WELL_ID,  WitsMetaName.WELL_NAME
            )

    def wellbores(self, wellId:str = None, wellboreId:str = None, is_show_full=False) -> snowpark.DataFrame:
        """
        Get WITSML Wellbore Metadata in the snowflake.snowpark.DataFrame format.
        Ref: https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/dataframe
        """
        df = self.metadata(
            table=WitsMetadataTableEnum.WITS_WELLBORE,
            col_filters=[
                (WitsMetaName.WELL_ID, wellId), 
                (WitsMetaName.WELLBORE_ID, wellboreId)
            ]
        )

        if is_show_full:
            return df
        else:
            return df.select(
                WitsMetaName.WELL_ID,  WitsMetaName.WELL_NAME,
                WitsMetaName.WELLBORE_ID, WitsMetaName.WELLBORE_NAME,
            )

    def logs(self, wellId:str = None, wellboreId:str = None, logId:str = None, longName:str = None, is_show_full=False) -> snowpark.DataFrame:
        """
        Get WITSML Logs Metadata in the snowflake.snowpark.DataFrame format.
        Ref: https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/dataframe
        """
        df = self.metadata(
            table=WitsMetadataTableEnum.WITS_LOG,
            col_filters=[
                (WitsMetaName.WELL_ID, wellId), 
                (WitsMetaName.WELLBORE_ID, wellboreId), 
                (WitsMetaName.LOG_ID, logId),
                (WitsMetaName.LOG_NAME, longName)
            ]
        )

        if is_show_full:
            return df
        else:
            return df.select(
                WitsMetaName.WELL_ID, WitsMetaName.WELL_NAME,
                WitsMetaName.WELLBORE_ID, WitsMetaName.WELLBORE_NAME,
                WitsMetaName.LOG_ID, WitsMetaName.LOG_NAME,
            )

    def logcurves(self, wellboreId:str, logId:str = None, logName:str=None, curveId:str = None, curveName:str = None, is_show_full=False) -> snowpark.DataFrame:
        """
        Get WITSML LogCurve Metadata in the snowflake.snowpark.DataFrame format.
        Ref: https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/dataframe
        """
        df = self.metadata(
            table=WitsMetadataTableEnum.WITS_LOGCURVE,
            col_filters=[
                (WitsMetaName.WELLBORE_ID, wellboreId), 
                (WitsMetaName.LOG_ID, logId), 
                (WitsMetaName.LOG_NAME, logName), 
                (WitsMetaName.CURVE_ID, curveId),
                (WitsMetaName.CURVE_NAME, curveName)
            ]
        )

        if is_show_full:
            return df
        else:
            return df.select(
                WitsMetaName.WELL_ID, WitsMetaName.WELL_NAME,
                WitsMetaName.WELLBORE_ID, WitsMetaName.WELLBORE_NAME, 
                WitsMetaName.LOG_ID, WitsMetaName.LOG_NAME, 
                WitsMetaName.CURVE_ID, WitsMetaName.CURVE_NAME, 
                WitsMetaName.UNIT,  WitsMetaName.DESCRIPTION
            )