from __future__ import absolute_import

import logging

# import base services into services package
try:
    from wellsrt_data_client.services.cores.az_ad_authz_service import AzAuthzService
except Exception as ex:
    logging.warning("Export AzAuthzService error - %s", ex)

# support Az Storage Account
try:
    from wellsrt_data_client.services.cores.az_storage_account_service import AzStorageAccountService
except Exception as ex:
    logging.warning("Export AzStorageAccountService error - %s", ex)

try:
    from wellsrt_data_client.services.cores.send_email_service import SendEmailService
except Exception as ex:
    logging.warning("Export SendEmailService error - %s", ex)
