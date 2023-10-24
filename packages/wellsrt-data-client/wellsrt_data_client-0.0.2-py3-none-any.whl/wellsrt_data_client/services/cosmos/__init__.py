from __future__ import absolute_import

import logging

# support Az Cosmos DB
try:
    from wellsrt_data_client.services.cosmos.az_cosmos_data_service import AzCosmosDataService, AzCosmosPartitionKeyModel
except Exception as ex:
    logging.warning("Export AzCosmosDataService error - %s", ex)