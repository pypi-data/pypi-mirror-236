import uvicorn

from sandbox_func.model.SandboxFuncManager import SandboxFuncManager
from sandbox_func.web import sandbox_app


class SandboxFuncServer:
    @classmethod
    def start(cls, repo_path: str, reload=False):
        SandboxFuncManager.read_repo_path(repo_path)
        uvicorn.run(sandbox_app.app, host="0.0.0.0", port=9000, log_level="info", reload=reload)
