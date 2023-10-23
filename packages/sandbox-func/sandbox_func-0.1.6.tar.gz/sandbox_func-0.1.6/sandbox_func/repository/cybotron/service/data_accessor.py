from sandbox_func.common.config.BaseURLConfig import BaseURLConfig
from sandbox_func.common.config.BusinessURLConfig import BusinessURLConfig, DataTypeEnum
from sandbox_func.common.config.LoginConfig import DefaultLoginConfig
from sandbox_func.repository.cybotron.model.metadataobj import GetRequest, GetResponse, GetListRequest, GetListResponse
from sandbox_func.repository.cybotron.service.common_access import CommonAccess


class DataAccessor(CommonAccess):
    def __init__(self):
        super().__init__()
        self.URL = BaseURLConfig.get_api_base_url(DefaultLoginConfig.get_env()) + BusinessURLConfig.get_url(
            DataTypeEnum.DATA)
        self.X_API_KEY = DefaultLoginConfig.get_api_key()

    async def get(self, req: GetRequest) -> GetResponse:
        """
        单条查询接口
        """
        result = await self.get_response(req, "get")
        data = {} if not result.get('data', "") else result['data']  # 查询结果为空, 返回空字典
        return GetResponse(data=data)

    async def getList(self, req: GetListRequest) -> GetListResponse:
        """
        分页查询接口
        """
        result = await self.get_response(req, "getList")
        return GetListResponse(data=result["data"], total=result["total"])
