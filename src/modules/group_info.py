from src.utils.config import config
from tortoise import fields
from tortoise.models import Model


class GroupInfo(Model):
    '''群信息处理'''
    group_id = fields.IntField(pk=True)
    '''群id'''
    group_name = fields.CharField(max_length=255, default='')
    '''群名'''
    sign_nums = fields.IntField(default=0)
    '''签到次数'''
    server = fields.CharField(max_length=255, default=config.default['server'])
    '''绑定服务器'''
    robot_status = fields.BooleanField(default=config.default['robot_status'])
    '''机器人状态'''
    robot_active = fields.IntField(default=config.default['robot_active'])
    '''活跃值'''
    welcome_status = fields.BooleanField(default=config.default['robot_welcome_status'])
    '''进群通知开关'''
    welcome_text = fields.JSONField(default=config.default['robot_welcome'])
    '''进群通知内容'''
    someoneleft_status = fields.BooleanField(default=config.default['robot_someone_left_status'])
    '''离群通知开关'''
    someoneleft_text = fields.JSONField(default=config.default['robot_someone_left'])
    '''离群通知内容'''
    goodnight_status = fields.BooleanField(default=config.default['robot_goodnight_status'])
    '''晚安通知开关'''
    goodnight_text = fields.JSONField(default=config.default['robot_goodnight'])
    '''晚安通知内容'''

    class Meta:
        table = "group_info"
        table_description = "管理QQ群信息"
