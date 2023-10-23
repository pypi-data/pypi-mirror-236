from sandbox_func.common.lang.dictclass import DictClass


class SandboxFunc(DictClass):
    id: str
    code: str
    name: str
    app_id: str
    async_func: bool    # 异步方法
    entry: str          # 执行路径
    run: callable       # 执行方法
