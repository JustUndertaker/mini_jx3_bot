import atexit
import sys as sys
from typing import Union

from loguru import _defaults
from loguru._logger import Core, Logger

from .config import config

logger = Logger(Core(), None, 0, False, False, True, False, True, None, {})
'''自定义的logger对象'''

# 清理
atexit.register(logger.remove)

# 日志文件记录格式
file_format = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    "{message}")

# 错误日志文件记录格式
error_format = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "[<c><u>{name}</u></c>] | "
    "<c>{function}:{line}</c>| "
    "{message}")

# 日志控制台记录格式
console_format = (
    "<g>{time:MM-DD HH:mm:ss}</g> "
    "[<lvl>{level}</lvl>] "
    "<c><u>{name}</u></c> | "
    "{message}")

# debug级别
loger_debug: bool = config.default['logger_debug']
if loger_debug:
    custom_level = 'DEBUG'
else:
    custom_level = 'INFO'


class Filter:

    def __init__(self) -> None:
        self.level: Union[int, str] = "DEBUG"

    def __call__(self, record):
        module_name: str = record["name"]
        module = sys.modules.get(module_name)
        if module:
            module_name = getattr(module, "__module_name__", module_name)
        name_list = module_name.split(".")
        length = len(name_list)
        if length < 2:
            record["name"] = name_list[0]
        elif length == 3:
            record["name"] = name_list[-1]
        else:
            record["name"] = name_list[-2]
        levelno = logger.level(self.level).no if isinstance(self.level,
                                                            str) else self.level
        return record["level"].no >= levelno


# 过滤器
default_filter = Filter()


# 添加到控制台
if _defaults.LOGURU_AUTOINIT and sys.stderr:
    logger.add(sys.stderr,
               filter=default_filter,
               format=console_format,
               level=custom_level
               )

# 添加到日志文件

path_cfg = config.path
debug_path = f"./{path_cfg['debug']}/"

logger.add(
    debug_path+"{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="10 days",
    level="DEBUG",
    format=file_format,
    filter=default_filter,
    encoding="utf-8"
)

info_path = f"./{path_cfg['info']}/"
logger.add(
    info_path+"{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="10 days",
    level="INFO",
    format=file_format,
    filter=default_filter,
    encoding="utf-8"
)

error_path = f"./{path_cfg['error']}/"
logger.add(
    error_path+"{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="10 days",
    level="ERROR",
    format=error_format,
    filter=default_filter,
    encoding="utf-8"
)
