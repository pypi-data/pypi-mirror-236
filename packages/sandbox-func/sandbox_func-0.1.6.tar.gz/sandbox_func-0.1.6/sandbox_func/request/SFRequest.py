from sandbox_func.common.lang.dictclass import DictClass


class SFRequest(DictClass):
    app_id: str
    func_id: str
    request_id: str
    input: DictClass
