import logging
import os.path

from sandbox_func.model.SandboxFuncManager import SandboxFuncManager

logger = logging.getLogger(__name__)
DEFAULT_PROJ_ROOT_DIR = '/mnt/scf'


class SandboxProjManager:

    def __init__(self, proj_root_dir: str = DEFAULT_PROJ_ROOT_DIR):
        self.proj_root_dir = proj_root_dir

    def walkJson(self):
        root_dir = self.proj_root_dir
        if not os.path.exists(root_dir):
            root_dir = DEFAULT_PROJ_ROOT_DIR

        if not os.path.exists(root_dir):
            logger.error(f'系统找不到沙盒函数目录{root_dir}')

        logger.info(f'沙盒函数运行时将从{root_dir}加载所有沙盒函数')
        for proj_name in os.listdir(root_dir):
            proj_dir = os.path.join(root_dir, proj_name)
            if os.path.isdir(proj_dir):
                logger.info(f'加载{proj_dir}沙盒函数项目')
                SandboxFuncManager.read_repo_path(proj_dir)
