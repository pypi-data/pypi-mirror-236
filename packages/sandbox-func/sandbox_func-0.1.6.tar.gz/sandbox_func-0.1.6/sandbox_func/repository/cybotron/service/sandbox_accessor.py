import asyncio
import json

from sandbox_func.common.config.BaseURLConfig import BaseURLConfig
from sandbox_func.common.config.BusinessURLConfig import BusinessURLConfig, DataTypeEnum
from sandbox_func.common.config.LoginConfig import DefaultLoginConfig
from sandbox_func.common.request.CybotronSyncClient import CybotronSyncClient
from sandbox_func.repository.cybotron.model.metadataobj import GetRequest
from sandbox_func.repository.cybotron.service.data_accessor import DataAccessor
from sandbox_func.request import SFResponse, SFRequest


class SandboxAccessor:

    def __init__(self):
        self.URL = BaseURLConfig.get_api_base_url(DefaultLoginConfig.get_env()) + BusinessURLConfig.get_url(
            DataTypeEnum.SANDBOX)

    def dispatchRequest(self, request: SFRequest) -> SFResponse:
        client = CybotronSyncClient()
        url = f"{self.URL}/{request.app_id}/{request.func_id}"
        response = SFResponse()
        try:
            res = client.send(url, 'POST', json=request.input)
            response.result = res['result']
            result_json = json.loads(res['result'])
            response.request_id = result_json["requestId"]
            return response
        except Exception as e:
            response.error = e
            return response

    def confirmAysncRequest(self, request: SFRequest) -> SFResponse:
        data_accessor = DataAccessor()
        get_req = GetRequest(
            appCode="metabase",
            tableCode="mb_async_job",
            id=request.request_id
        )
        response = SFResponse()
        try:
            get_res = asyncio.run(data_accessor.get(get_req))
            response.request_id = request.request_id
            response.result = get_res.data
            return response
        except Exception as e:
            response.error = e
            return response
