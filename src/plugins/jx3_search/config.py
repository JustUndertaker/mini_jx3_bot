from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, validator

"""剑网三查询插件配置"""


class JX3PROFESSION(Enum):
    """剑网三心法枚举"""

    无方 = {"无方", "药宗", "药宗输出", "药宗dps"}
    灵素 = {"灵素", "药奶", "奶药", "药宗奶妈"}
    太玄经 = {"太玄经", "衍天宗", "衍天", "太玄"}
    隐龙诀 = {
        "隐龙诀",
        "隐龙",
        "凌雪阁",
        "凌雪",
    }
    凌海诀 = {
        "凌海诀",
        "凌海",
        "蓬莱",
        "伞爹",
    }
    北傲诀 = {"北傲诀", "北傲", "霸刀", "刀爹", "北傲决"}
    莫问 = {"莫问", "长歌输出", "长歌dps", "长歌"}
    相知 = {"相知", "长歌治疗", "长歌奶", "歌奶", "奶歌"}
    分山劲 = {"分山劲", "分山", "苍云输出", "苍云dps", "苍云"}
    铁骨衣 = {"铁骨衣", "铁骨", "苍云T", "苍云t", "铁王八"}
    笑尘诀 = {"笑尘诀", "笑尘", "丐帮", "丐丐", "要饭的", "笑尘诀"}
    焚影圣诀 = {"焚影圣诀", "焚影", "明教dps", "明教输出", "明教", "喵喵", "焚影圣决"}
    明尊琉璃体 = {"明尊琉璃体", "明尊", "明教T", "明教t", "喵T", "喵t"}
    惊羽诀 = {"惊羽诀", "惊羽", "鲸鱼"}
    天罗诡道 = {"天罗诡道", "田螺", "天罗"}
    毒经 = {"毒经", "读经", "五毒dps", "五毒输出", "五毒"}
    补天诀 = {"补天诀", "补天", "奶毒", "毒奶", "补天决"}
    山居剑意 = {"山居剑意", "问水诀", "藏剑", "黄鸡", "山居", "问水", "鸡哥", "风车侠"}
    傲血战意 = {"傲血战意", "傲雪", "傲血", "天策dps", "天策输出", "天策", "哈士奇"}
    铁牢律 = {"铁牢律", "铁牢", "策T", "策t", "天策T", "天策t"}
    太虚剑意 = {"太虚剑意", "太虚", "剑纯", "渣男"}
    紫霞功 = {"紫霞功", "紫霞", "气纯"}
    易筋经 = {
        "易筋经",
        "易筋",
        "和尚dps",
        "和尚输出",
        "大师dps",
        "大师输出",
        "少林dps",
        "少林输出",
        "和尚",
        "少林",
        "光头",
    }
    洗髓经 = {"洗髓经", "洗髓", "和尚T", "和尚t", "大师t", "大师T", "少林t", "少林T"}
    冰心诀 = {"冰心诀", "冰心", "冰秀", "七秀dps", "七秀输出", "七秀", "秀秀", "冰心决"}
    云裳心经 = {"云裳心经", "云裳", "秀奶", "奶秀"}
    花间游 = {"花间游", "花间", "万花dps", "万花输出", "万花", "花花"}
    离经易道 = {
        "离经易道",
        "离经",
        "奶花",
        "花奶",
    }
    孤锋诀 = {"孤锋诀", "刀宗", "刀爹", "鬼子", "孤峰", "孤锋"}

    @classmethod
    def get_profession(cls, name: str) -> Optional[str]:
        """通过别名获取职业名称"""
        for profession in cls:
            if name in profession.value:
                return profession.name
        return None


class FireWorkRecord(BaseModel, extra=Extra.ignore):
    """烟花记录"""

    server: str
    """服务器名"""
    name: str
    """烟花名"""
    map: str
    """地图名"""
    sender: str
    """发送方"""
    recipient: str
    """接收方"""
    time: str
    """时间"""
    times: int = 1
    """计数"""

    @validator("time", pre=True)
    def check_status(cls, v):
        return date.fromtimestamp(v).strftime("%Y-%m-%d")

    def __eq__(self, other: "FireWorkRecord"):
        return (
            self.server == other.server
            and self.map == other.map
            and self.name == other.name
            and self.sender == other.sender
            and self.recipient == other.recipient
            and self.time == other.time
        )
