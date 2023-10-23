import logging
from collections import UserDict
from enum import Enum
from pathlib import Path

from sandbox_func.common.config.LogConfig import DEFAULT_LOG_FILE
from sandbox_func.common.config.LoginConfig import DefaultLoginConfig
from sandbox_func.service.cybotron.log_accessor import LogAccessor


class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Log(UserDict):
    trace_id: str
    app_id: str
    app_version_id: str
    func_id: str
    creator: str
    level: str
    message: str


class AwLogger:
    """autowork log warapper"""

    cybotron_access_info: dict = {}

    @classmethod
    def getLogger(cls, filename: str, level: LogLevel = LogLevel.INFO):
        logger = logging.getLogger(filename)
        if level is None:
            logger.setLevel('INFO')
        else:
            logger.setLevel(level.value)

        logfile = Path().home().joinpath(DEFAULT_LOG_FILE)
        logdir = logfile.parent
        if not logdir.exists():
            logdir.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d [%(levelname)s] %(filename)s:%(lineno)s - %(""message)s",
            datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 如果是debug模式，信息入库metabase.mb_sandbox_debug_log
        if DefaultLoginConfig.get_debug():
            db_handler = DBLogHandler()
            db_handler.setFormatter(formatter)
            logger.addHandler(db_handler)

        return logger


class DBLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record: logging.LogRecord):
        msg = record.getMessage()
        trace_id = msg.split('-')[0]
        real_msg = msg.split('-')[1]
        cybotron_access_info = AwLogger.cybotron_access_info[trace_id]
        log = Log(
            trace_id=cybotron_access_info['trace_id'],
            app_id=cybotron_access_info['app_id'],
            app_version_id=cybotron_access_info['app_version_id'],
            func_id=cybotron_access_info['func_id'],
            creator=cybotron_access_info['creator'],
            level=record.levelno,
            message=real_msg
        )

        try:
            LogAccessor.send_log(log.data)
        except Exception as e:
            print(e)
