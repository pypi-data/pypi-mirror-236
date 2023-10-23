import json
import os

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from sandbox_func.common.log.AwLogger import AwLogger, Log
from sandbox_func.common.lang import logger_setting
from sandbox_func.request.SFRequest import SFRequest
from sandbox_func.service.SandboxFuncService import SandboxFuncService
from sandbox_func.service.SandboxCallbackService import SandboxCallbackService

logger_setting.init()
logger = AwLogger.getLogger(__name__)
app = FastAPI(title="Autowork Sandbox Function")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {
        "pid": os.getpid()
    }


@app.post("/sandbox/call/{app_id}/{func_id}/local")
async def call_sandbox_func_local(app_id: str, func_id: str, req: Request):
    """本地调试接口"""

    global trace_id
    try:
        data = await req.body()
        if data != b'':
            data = await req.json()

        debug = data['debug']
        trace_id = debug['traceId']
        cybotron_access_info = Log(
            trace_id=trace_id,
            app_id=debug['appId'],
            app_version_id=debug['appVersionId'],
            func_id=func_id,
            creator=debug['creator']
        )
        AwLogger.cybotron_access_info[trace_id] = cybotron_access_info

        logger.info(f'{trace_id}-沙盒函数运行时调用本地云函数，应用编号：{app_id}, 函数编号：{func_id}, 参数：{data}')
        request = SFRequest(app_id=app_id, func_id=func_id, input=data)
        service = SandboxFuncService()
        response = await service.call(request)

        if response.result:
            return response.result
        elif response.error:
            return {"message": str(response.error), "success": False}
    except BaseException as e:
        logger.error(f'{trace_id}-沙盒函数运行时调用本地云函数报错，应用编号：{app_id}, 函数编号：{func_id}, 错误信息：{e}')
        return {"message": str(e), "success": False}


@app.post("/sandbox/call/{app_id}/{func_id}")
async def call_sandbox_func(app_id: str, func_id: str, req: Request):
    """ 线上同步接口 """
    try:
        service = SandboxFuncService()
        data = await req.body()
        if data != b'':
            data = await req.json()

        request = SFRequest(app_id=app_id, func_id=func_id, input=data)
        response = await service.call(request)

        if response.result:
            return response.result
        elif response.error:
            return {"message": str(response.error), "success": False}
    except BaseException as e:
        logger.exception(e)
        return {"message": str(e), "success": False}


@app.post("/event-invoke")
async def call_sandbox_func_async(req: Request):
    """线上异步接口"""
    try:
        service = SandboxFuncService()
        data = await req.json()
        logger.info(data)
        param = json.loads(data['body'])
        logger.info(f'收到沙盒函数请求，请求参数：{param}')
        if param is None or param['appId'] is None or param['funcId'] is None:
            return {"message": '参数错误，请指定沙盒函数的appId与funcId', "success": False}

        request = SFRequest(app_id=param['appId'], func_id=param['funcId'], input=param['input'])
        response = await service.call(request)

        # 如果是异步执行，且请求参数指定了hook，则进行回调
        SandboxCallbackService.callback(request, response)

        if response.result:
            return response.result
        elif response.error:
            return {"message": str(response.error), "success": False}
    except BaseException as e:
        logger.exception(f'处理沙盒函数调用报错，报错信息：{e}')
        return {"message": str(e), "success": False}
