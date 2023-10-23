import asyncio
import json
import logging

from tencentcloud.common import credential
from tencentcloud.scf.v20180416 import scf_client, models

from sandbox_func.common.config.TencentConfig import SECRET_ID, SECRET_KEY
from sandbox_func.common.lang.async_requests import AsyncRequests
from sandbox_func.common.lang.singleton import SingletonMeta
from sandbox_func.request.SFEventRequest import SFEventRequest
from sandbox_func.request.SFExtRequest import SFExtRequest
from sandbox_func.request.SFWebRequest import SFWebRequest
from sandbox_func.request.SFResponse import SFResponse

logger = logging.getLogger(__name__)


class SandboxFuncServiceForTencent(metaclass=SingletonMeta):

    def __init__(self):
        pass

    def call(self, request: SFExtRequest) -> SFResponse:
        if request.func_type == 'web':
            return self.processWeb(SFWebRequest(request))
        else:
            return self.processEvent(SFEventRequest(request))

    def processEvent(self, request: SFEventRequest) -> SFResponse:
        response = SFResponse()
        try:
            cred = credential.Credential(SECRET_ID, SECRET_KEY)
            client = scf_client.ScfClient(cred, request.func_region, None)

            invoke_request = models.InvokeRequest()
            params = {
                "FunctionName": request.func_id,
                "ClientContext": request.input
            }
            invoke_request.from_json_string(json.dumps(params))

            # 返回的resp是一个InvokeResponse的实例，与请求对象对应
            resp = client.Invoke(invoke_request)
            response.result = resp.Result
            response.request_id = resp.RequestId
            print(response)
            return response
        except Exception as e:
            logger.exception(e)
            response.error = str(e)
            return response

    def processWeb(self, request: SFWebRequest) -> SFResponse:
        client = AsyncRequests(base_url=request.apigw_url)
        request = client.build_request(method=request.http_method, url=request.func_path, data=request.input)
        response = SFResponse()
        try:
            resp = asyncio.run(client.send(request))
            if resp.status_code == 200 and resp.is_success:
                response.result = resp.text
            else:
                response.error = resp.text
            print(response)
            return response
        except Exception as e:
            logger.exception(e)
            response.error = str(e)
            return response
