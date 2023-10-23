import json

from sandbox_func.common.config.LoginConfig import LoginConfig
from sandbox_func.common.config.BaseURLConfig import BaseURLConfig
from sandbox_func.common.lang.async_requests import AsyncRequests


class CybotronClient:
    def __init__(self, throw_exception=True):
        self.throw_exception = throw_exception

    async def get(self, url, json=None):
        return await self.send(url, method="get", json=json)

    async def send(self, url, method, _json=None):
        login_config = LoginConfig()
        env = login_config.get_env()
        api_key = login_config.get_api_key()
        base_url = BaseURLConfig.get_api_base_url(env)

        client = AsyncRequests(base_url=base_url)
        data = json.dumps(_json)
        request = client.build_request(method=method, url=url, data=data, headers=CybotronClient.__get_headers(api_key))

        response = await client.send(request)
        response_json = response.json()

        if self.throw_exception and response_json.get("errorMessage"):
            raise Exception(response_json.get("errorMessage"))

        return response_json

    def post(self, url, json=None):
        return self.send(url, method="post", json=json)

    @staticmethod
    def __get_headers(api_key):
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': api_key
        }
        return headers
