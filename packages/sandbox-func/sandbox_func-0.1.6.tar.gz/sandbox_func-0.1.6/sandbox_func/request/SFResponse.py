from sandbox_func.request.SFResponseJob import SFResponseJob
from sandbox_func.common.lang.dictclass import DictClass


class SFResponse(DictClass):
    result: any
    request_id: str
    error: any
    job: SFResponseJob = SFResponseJob()
