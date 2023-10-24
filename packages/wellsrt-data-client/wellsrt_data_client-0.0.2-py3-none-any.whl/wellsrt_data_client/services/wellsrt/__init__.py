from __future__ import absolute_import

import logging

# support Snowflake
try:
    from wellsrt_data_client.services.wellsrt.wits_metadata_service import WitsMetadataService, WitsMetadataTableEnum, WitsMetaName
except Exception as ex:
    logging.warning("Export wits_metadata_service error - %s", ex)


# support azure-kusto-data
try:
    from wellsrt_data_client.services.wellsrt.wits_data_service import WitsDataService
except Exception as ex:
    logging.warning("Export wits_data_service error - %s", ex)