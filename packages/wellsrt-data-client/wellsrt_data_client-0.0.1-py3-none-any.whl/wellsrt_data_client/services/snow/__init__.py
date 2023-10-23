from __future__ import absolute_import

import logging

# support Snowflake
try:
    from wellsrt_data_client.services.snow.snow_data_service import SnowDataService
except Exception as ex:
    logging.warning("Export SnowDataService error - %s", ex)