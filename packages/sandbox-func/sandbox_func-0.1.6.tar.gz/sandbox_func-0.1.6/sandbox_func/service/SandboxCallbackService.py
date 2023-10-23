import json

import httpx

from sandbox_func.request import SFResponse, SFRequest
from sandbox_func.common.log.AwLogger import AwLogger

logger = AwLogger.getLogger(__name__)


class SandboxCallbackService:
    """异步任务回调处理，如果request里包含hook信息，则进行回调"""

    def __init__(self, request: SFRequest, response: SFResponse):
        self.req = request
        self.res = response

    @staticmethod
    def callback(req: SFRequest, res: SFResponse):
        hook = req.input.get('hook')
        if hook is not None:
            callback_url = dict(hook).get('url')
            data = {"result": res.result, "input": req.input, "progress": res.job.job_progress,
                    "success": res.job.job_success, "error": res.job.job_error}
            logger.info(f'异步请求回调， 回调地址：{callback_url}， 回调参数：{data}')
            client = httpx.Client()
            try:
                client.post(callback_url,
                            json=json.dumps(data, ensure_ascii=False, default=lambda dictclass: dictclass.data))
            except Exception as e:
                logger.error(f"回调处理报错，回调地址：{callback_url}, 回到参数：{data}, 报错信息：{e}")
