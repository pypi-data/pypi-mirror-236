import json
import logging
import sys
from pathlib import Path

from sandbox_func.common.lang.moduleutil import ModuleUtil
from sandbox_func.model.SandboxApp import SandboxApp
from sandbox_func.model.SandboxFunc import SandboxFunc
from sandbox_func.model.SandboxRepo import SandboxRepo

logger = logging.getLogger(__name__)


class SandboxFuncManager:
    func_mapping = {}  # type: {str: SandboxFunc}
    apps = []

    @classmethod
    def read_repo_path(cls, repo_path: str):
        json_path = repo_path + "/sandbox_function.json"
        repo = cls.read_json_file(json_path)
        if repo is not None:
            repo.path = repo_path
            cls.register_repo(repo)

    @classmethod
    def read_json_file(cls, json_path: str):
        json_path = Path(json_path)
        if not json_path.exists():
            logger.error(f"应用注册文件不存在: {json_path}")
            return
        with open(json_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            repo = SandboxRepo(json_data)
            apps = []
            for app in repo.apps:
                apps.append(SandboxApp(app))
            repo.apps = apps
            return repo

    @classmethod
    def register_repo(cls, repo: SandboxRepo):
        # 将repo加入源码路径，以便import
        sys.path.append(repo.path)
        for app in repo.apps:
            cls.register_app(SandboxApp(app))

    @classmethod
    def register_app(cls, app: SandboxApp):
        cls.apps.append(app)
        for func in app.funcs:
            func = SandboxFunc(func)
            key = f"{app.id}.{func.id}"
            cls.func_mapping[key] = func

    @classmethod
    def get_func(cls, app_id: str, func_id: str) -> SandboxFunc:
        key = f"{app_id}.{func_id}"
        func = cls.func_mapping.get(key)
        if func:
            entry = func.entry
            if not func.run:
                func.run = ModuleUtil.get_func(entry)
        return func

    @classmethod
    def clear(cls):
        cls.func_mapping.clear()
        cls.apps.clear()
