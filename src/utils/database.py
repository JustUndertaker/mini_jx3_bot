from tortoise import Tortoise

from .config import path_config
from .log import logger


async def database_init():
    '''
    初始化建表
    '''
    logger.debug('正在注册数据库')
    path = path_config.data
    database_path = f"./{path}/data.db"
    db_url = f'sqlite://{database_path}'
    # 这里填要加载的表
    models = [
        'src.modules.group_info',
        'src.modules.plugin_info',
        'src.modules.user_info',
        'src.modules.ticket_info',
        'src.modules.search_record'
    ]
    modules = {"models": models}
    await Tortoise.init(db_url=db_url, modules=modules)
    await Tortoise.generate_schemas()
    logger.info('<g>数据库初始化成功。</g>')
