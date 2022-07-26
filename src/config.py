from pathlib import Path

from nonebot import get_driver
from pydantic import BaseModel, Extra, Field


class Jx3ApiConfig(BaseModel, extra=Extra.ignore):
    """
    jx3api的配置
    """

    ws_path: str = Field("", alias="jx3api_ws_path")
    """ws连接地址"""
    ws_token: str = Field("", alias="jx3api_ws_token")
    """ws的token"""
    api_url: str = Field("", alias="jx3api_url")
    """主站的url"""
    api_token: str = Field("", alias="jx3api_token")
    """主站的token"""


class NlpConfig(BaseModel, extra=Extra.ignore):
    """
    nlp配置
    """

    secretId: str = Field("", alias="nlp_secretid")
    secretKey: str = Field("", alias="nlp_secretkey")


class VoiceConfig(BaseModel, extra=Extra.ignore):
    """
    阿里云语音配置
    """

    appkey: str = Field("", alias="voice_appkey")
    access: str = Field("", alias="voice_access")
    secret: str = Field("", alias="voice_secret")
    voice: str = Field("Aitong", alias="voice_voice")
    """发言人"""
    format: str = Field("mp3", alias="voice_format")
    """编码格式"""
    sample_rate: int = Field(16000, alias="voice_sample_rate")
    """采样率"""
    volume: int = Field(50, alias="voice_volume")
    """音量"""
    speech_rate: int = Field(0, alias="voice_speech_rate")
    """语速"""
    pitch_rate: int = Field(0, alias="voice_pitch_rate")
    """音调"""


class WeatherConfig(BaseModel, extra=Extra.ignore):
    """
    天气插件配置
    """

    api_key: str = Field("", alias="weather_api_key")
    api_type: int = Field(0, alias="weather_api_type")


class DefaultConfig(BaseModel, extra=Extra.ignore):
    """
    默认设置
    """

    server: str = Field("幽月轮", alias="default_server")
    """默认绑定区服"""
    access_firend: bool = Field(True, alias="default_access_firend")
    """是否接受好友请求"""
    access_group: bool = Field(True, alias="default_access_group")
    """是否接受群请求"""
    robot_status: bool = Field(True, alias="default_robot_status")
    """机器人开关"""
    robot_active: int = Field(10, alias="default_robot_active")
    """机器人活跃"""
    robot_welcome_status: bool = Field("", alias="default_robot_welcome_status")
    """进群欢迎开关"""
    robot_welcome: str = Field(True, alias="defualt_robot_welcome")
    """进群欢迎语"""
    robot_someone_left_status: bool = Field(
        False, alias="defualt_robot_someone_left_status"
    )
    """群友离开说话开关"""
    robot_someone_left: str = Field("", alias="defualt_robot_someone_left")
    """群友离开内容"""
    robot_goodnight_status: bool = Field(True, alias="defulat_robot_goodnight_status")
    """晚安通知开关"""
    robot_goodnight: str = Field("", alias="defulat_robot_goodnight")
    """晚安通知内容"""


class PathConfig(BaseModel, extra=Extra.ignore):
    """
    路径设置
    """

    data: str = Field("", alias="path_data")
    """数据文件"""
    logs: str = Field("", alias="path_logs")
    """日志文件"""
    templates: str = Field("", alias="path_templates")
    """html模板文件"""


class LogsConfig(BaseModel, extra=Extra.ignore):
    """
    日志设置
    """

    is_console: bool = Field(True, alias="logs_is_console")
    """是否输出到控制台"""
    console_level: str = Field("INFO", alias="logs_console_level")
    """控制台输出等级"""
    is_file_info: bool = Field(True, alias="logs_is_file_info")
    """是否输出info文件"""
    is_file_debug: bool = Field(True, alias="logs_is_file_debug")
    """是否输出debug文件"""
    is_file_error: bool = Field(True, alias="logs_is_file_error")
    """是否输出error文件"""


# 创建配置实例
config = get_driver().config
jx3api_config = Jx3ApiConfig.parse_obj(config)
"""jx3api的配置"""
nlp_config = NlpConfig.parse_obj(config)
"""nlp配置"""
voice_config = VoiceConfig.parse_obj(config)
"""阿里云语音配置"""
weather_config = WeatherConfig.parse_obj(config)
"""天气插件配置"""
default_config = DefaultConfig.parse_obj(config)
"""默认设置"""
path_config = PathConfig.parse_obj(config)
"""路径设置"""
logs_config = LogsConfig.parse_obj(config)
"""日志设置"""

# 创建文件夹
_workdir = Path.cwd()

# data文件夹
_datadir = _workdir / path_config.data
_datadir.mkdir(parents=True, exist_ok=True)

# logs文件夹
_logdir = _workdir / path_config.logs
_info = _logdir / "info"
_info.mkdir(parents=True, exist_ok=True)
_debug = _logdir / "debug"
_debug.mkdir(parents=True, exist_ok=True)
_error = _logdir / "error"
_error.mkdir(parents=True, exist_ok=True)
