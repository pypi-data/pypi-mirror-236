import uvicorn
import sys

from sandbox_func.model.SandboxProjManager import SandboxProjManager
from sandbox_func.web import sandbox_app

if __name__ == '__main__':
    if len(sys.argv) > 1:
        proj_manager = SandboxProjManager(sys.argv[1])
    else:
        proj_manager = SandboxProjManager()
    proj_manager.walkJson()

    uvicorn.run(sandbox_app.app, host="0.0.0.0", port=9000, log_level="info")
