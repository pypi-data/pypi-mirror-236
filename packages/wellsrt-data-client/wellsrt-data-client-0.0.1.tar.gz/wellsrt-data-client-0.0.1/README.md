# WellsRT Data Client library

The `wellsrt-data-client` library supports datasources  integration:

### Core Services

- Support application configuration - [EnvVariables](./wellsrt_data_client/commons/env_variables.py) - in the `.\conf\tasks\app_config_dev|staging|prod.yml` file, and secret in the Local System environement (`.env` file) or Az KeyVault in the Databricks environement.
- Support Azure AD Authentication - [AzAuthzService](./wellsrt_data_client/services/cores/az_ad_authz_service.py) - to retrieve Azure service's JWT Token.
- Support Az Storage Account - [AzStorageAccountService](./wellsrt_data_client/services/cores/az_storage_account_service.py) - to Mount/UnMount a Az Storage Container at the runtime.
- Support email out - [SendEmailService](./wellsrt_data_client/services/cores/send_email_service.py) - to send an email from Databrick Jobs by using MuleSoft SMTP API.
- Support Azure CosmosDB integration - [AzCosmosDataService](./wellsrt_data_client/services/cosmos/az_cosmos_data_service.py)
- Support Azure ADX integration - [AzAdxDataService](./adx/az_adx_data_service.py)
- Support Snowflake integration with Snowpark - [SnowDataService](./wellsrt_data_client/services/snow/snow_data_service.py)

### WITS Services


- WITS Realtime Metadata - [WitsMetadataService](./wellsrt_data_client/services/wellsrt/wits_metadata_service.py) to load Wells, Wellbores, Logs, LogCurves metadata to `snowpark.DataFrame` object.
- WITS Realtime Data - [WitsDataService](./wellsrt_data_client/services/wellsrt/wits_data_service.py) to load LogCurves data to `pd.DataFrame` object.

While using this project, you need Python 3.10 and `pip` or `conda` for package management.

## Wells Data Pipeline Cores library setup

The [wellsrt-data-client](https://github.com/ExxonMobil/wellsrt-data-client-py) library will require the following dependencies to enable supported features/integrations in the [setup.py](./setup.py):

## Requirements.

- Python 3.10+
- Setup Development Environment [README-env.md](./docs/README-env.md)
- Setup Development Variables [README-vars.md](./docs/README-vars.md)

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

#### Option 1: Using Git Hub Access Token

```sh
pip install git+https://github.com/ExxonMobil/wellsrt-data-client-py.git
```

#### Option 2: Using Git Hub SSH Key

You need to make sure to setup GitHub with SSH by following guideline below

- [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- [Testing your SSH connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)

```sh
pip install git+ssh://git@github.com/ExxonMobil/wellsrt-data-client-py.git
```

The libraries dependency describe at [README-libs.md](./docs/README-libs.md)

Then import the package:
```python
import wellsrt_data_client
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import wellsrt_data_client
```

### Tools - Python symtax checking

- stop the build if there are Python syntax errors or undefined names

    ```
    flake8 ./wellsrt_data_client --count --select=E9,F63,F7,F82 --show-source --statistics

    flake8 ./ipy-notebooks --count --select=E9,F63,F7,F82 --show-source --statistics
    ```

- exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide

    ```
    flake8 ./wellsrt_data_client --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

    flake8 ./ipy-notebooks --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    ```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

### Setup Configuration and EnvVariables 

```python
from __future__ import print_function
from pprint import pprint
from wellsrt_data_client.common import enable_logging

from wellsrt_data_client.commons import DevUtils, EnvVariables
# there is NO dbutils on local machine

conf = DevUtils().read_dev_config()
env_vars = EnvVariables(conf=conf)

# Enable logging
enable_logging()

```

### WITS Metadata and Data Service

```python

from wellsrt_data_client.services.wellsrt import WitsDataService, WitsMetadataService, WitsMetaName

from datetime import datetime, timezone

# Create WITS Metadata and Data Service

wits_data_service = WitsDataService(env_vars=env_vars)

wits_metadata_service = WitsMetadataService(env_vars=env_vars)

# Sample WellboreId and LogName

wellbore_id = "us_28761607_wb1"
log_name = "Log #dfr_time_1s"

# Load log_curves metadata to snowpark.DataFrame OR pd.DataFrame

df_logcurves = wits_metadata_service.logcurves(wellboreId=wellbore_id, logName=log_name)

df_logcurves.to_pandas()

# Load logs_data from realtime database to pd.DataFrame
utc_format = '%Y-%m-%dT%H:%M:%S%z'
start_time = datetime.strptime("2023-08-14T23:20:23Z", utc_format)
end_time = datetime.strptime("2023-08-14T23:37:23Z", utc_format)

wellbore_id = "us_28761607_wb1"
log_name = "Log #dfr_time_1s"
log_curve_names = ["adtsp", "az", "bdep", "dept"]

df_logs_data = wits_data_service.query_dtimes_data(
    wellboreId=wellbore_id, 
    logName=log_name, 
    curveNames=log_curve_names, 
    startTime=start_time, 
    endTime=end_time
)


```

## Sample Code

- [Sample WellsRT Wells & Wellbores Metadata](./ipy-notebooks/test_wellsrt_metadata_service_wits_wellbores.ipynb)
- [Sample WellsRT Logs & LogCurves Metadata](./ipy-notebooks/test_wellsrt_metadata_service_wits_logs.ipynb)
- [Sample WellsRT DTime LogCurve Data in the Realtime Database](./ipy-notebooks/test_wellsrt_data_service_dtimes.ipynb)
- [Sample WellsRT DTime Query LogCurve Data from the Realtime Database](./ipy-notebooks/test_wellsrt_data_service_dtimes_query.ipynb)

## Author

- Tung.Nguyen


