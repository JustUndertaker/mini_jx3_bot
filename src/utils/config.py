import os
from typing import Optional, Union

import yaml

config: Optional[dict[str, dict[str, Union[str, int, bool]]]] = None
'''全局配置字典'''


def config_init():
    '''
    初始化读取配置文件，需要在所有项目之前启动
    '''
    global config
    with open('config.yml', 'r', encoding='utf-8') as f:
        cfg = f.read()
        config = yaml.load(cfg, Loader=yaml.FullLoader)

    # 判断项目目录是否存在
    path = config.get('path')
    data = path.get('data')
    if not os.path.exists(data):
        os.makedirs(data)
    log = path.get('log')
    info = log+'info'
    if not os.path.exists(info):
        os.makedirs(info)
    debug = log+'debug'
    if not os.path.exists(debug):
        os.makedirs(debug)
    error = log+'error'
    if not os.path.exists(error):
        os.makedirs(error)
