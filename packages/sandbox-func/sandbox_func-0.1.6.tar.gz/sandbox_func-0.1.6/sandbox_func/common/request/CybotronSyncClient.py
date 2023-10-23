import asyncio

from sandbox_func.common.request.CybotronClient import CybotronClient


class CybotronSyncClient:
    """
    赛博坦同步接口，方便命令行工具等没有异步条件的代码中使用
    """

    def __init__(self, throw_exception=True):
        self.throw_exception = throw_exception
        self.client = CybotronClient(throw_exception)

    def get(self, url, json=None):
        return self.send(url, method="get", json=json)

    def send(self, url, method, json=None):
        return asyncio.run(self.client.send(url, method, json))

    def post(self, url, json=None):
        return self.send(url, method="post", json=json)
