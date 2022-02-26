from pathlib import Path
from typing import Dict, Union

import yaml


class Config():
    '''配置文件类'''

    def __new__(cls, *args, **kwargs):
        '''单例'''
        if not hasattr(cls, '_instance'):
            orig = super(Config, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance

    def __getattr__(self, item) -> Dict[str, Union[str, int, bool]]:
        '''获取配置'''
        value = self._config.get(item)
        if value:
            return value
        raise AttributeError("未找到该配置字段，请检查config.yml文件！")

    def __init__(self):
        '''初始化'''
        workdir = Path.cwd()
        config_file = workdir / "config.yml"
        with open(config_file, 'r', encoding='utf-8') as f:
            cfg = f.read()
            self._config: dict = yaml.load(cfg, Loader=yaml.FullLoader)

        # 创建目录
        path: dict = self._config.get('path')

        # data文件夹
        data: str = path.get('data')
        datadir = workdir / data
        if not Path.exists(datadir):
            Path.mkdir(datadir, parents=True)

        # log文件夹
        info: str = path.get('info')
        infodir = workdir / info
        if not Path.exists(infodir):
            Path.mkdir(infodir, parents=True)

        debug: str = path.get('debug')
        debugdir = workdir / debug
        if not Path.exists(debugdir):
            Path.mkdir(debugdir, parents=True)

        error: str = path.get('error')
        errordir = workdir / error
        if not Path.exists(errordir):
            Path.mkdir(errordir, parents=True)


config = Config()
"""
配置文件模块，用于读取项目内的config.yml文件配置内容
使用方法:
```
from src.utils.config import config

>>>config.your_config_key
```
"""
