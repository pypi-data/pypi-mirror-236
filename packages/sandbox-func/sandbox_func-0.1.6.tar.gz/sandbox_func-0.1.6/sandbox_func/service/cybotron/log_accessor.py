import json

import httpx

from sandbox_func.common.request.CybotronClient import CybotronClient
from sandbox_func.common.config.BaseURLConfig import BaseURLConfig
from sandbox_func.common.config.BusinessURLConfig import BusinessURLConfig, DataTypeEnum
from sandbox_func.common.config.LogConfig import LOG_APP_CODE, LOG_TABLE_CODE, CYBOTRON_API_KEY
from sandbox_func.common.config.LoginConfig import DefaultLoginConfig, LoginConfig


class LogAccessor:

    @staticmethod
    def send_log(log_message: dict) -> bool:
        base_url = BaseURLConfig.get_api_base_url(DefaultLoginConfig.get_env())
        business_url = f"{base_url}{BusinessURLConfig.get_url(DataTypeEnum.DATA)}/{LOG_APP_CODE}/{LOG_TABLE_CODE}/create"

        req = {
            "values": log_message,
            "options": {
                "conflictToUpdate": False
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': CYBOTRON_API_KEY
        }

        client = httpx.Client()
        res = client.post(business_url, data=json.dumps(req), headers=headers)
        if res.is_success:
            return True
        else:
            return False
