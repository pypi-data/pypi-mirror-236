import logging

from sandbox_func.common.lang.singleton import SingletonMeta
from sandbox_func.model.SandboxFuncManager import SandboxFuncManager
from sandbox_func.request.SFRequest import SFRequest
from sandbox_func.request.SFResponse import SFResponse

logger = logging.getLogger(__name__)


class SandboxFuncService(metaclass=SingletonMeta):
    def __init__(self):
        pass

    async def call(self, request: SFRequest) -> SFResponse:
        func = SandboxFuncManager.get_func(request.app_id, request.func_id)
        if not func or not func.run:
            logger.error(f'沙盒函数缓存里找不到app_id={request.app_id}, func_id={request.func_id}')
            raise Exception(f"app_id={request.app_id}, func_id={request.func_id} not found")
        response = SFResponse()
        try:
            result = await func.run(request, response)
            if result:
                response.result = result
            return response
        except Exception as e:
            logger.exception(e)
            response.error = str(e)
            return response

    # TODO 加个异步回调接口，反馈进度
