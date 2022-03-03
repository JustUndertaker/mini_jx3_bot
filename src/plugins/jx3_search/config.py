from dataclasses import dataclass
from enum import Enum
from typing import Optional

'''剑网三查询插件配置'''


class JX3PROFESSION(Enum):
    '''剑网三心法枚举'''
    无方 = {"无方", "药宗", "药宗输出", "药宗dps"}
    灵素 = {"灵素", "药奶", "奶药", "药宗奶妈"}
    太玄经 = {"太玄经", "衍天宗", "衍天", "太玄"}
    隐龙诀 = {"隐龙诀", "隐龙", "凌雪阁", "凌雪", }
    凌海诀 = {"凌海诀", "凌海", "蓬莱", "伞爹", }
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
    易筋经 = {"易筋经", "易筋", "和尚dps", "和尚输出", "大师dps", "大师输出", "少林dps", "少林输出", "和尚", "少林", "光头"}
    洗髓经 = {"洗髓经", "洗髓", "和尚T", "和尚t", "大师t", "大师T", "少林t", "少林T"}
    冰心诀 = {"冰心诀", "冰心", "冰秀", "七秀dps", "七秀输出", "七秀", "秀秀", "冰心决"}
    云裳心经 = {"云裳心经", "云裳", "秀奶", "奶秀"}
    花间游 = {"花间游", "花间", "万花dps", "万花输出", "万花", "花花"}
    离经易道 = {"离经易道", "离经", "奶花", "花奶", }

    @classmethod
    def get_profession(cls, name: str) -> Optional[str]:
        '''通过别名获取职业名称'''
        for profession in cls:
            if name in profession.value:
                return profession.name
        return None


DAILIY_LIST = {
    "一": "帮会跑商：阴山商路(10:00)\n阵营祭天：出征祭祀(19:00)\n",
    "二": "阵营攻防：逐鹿中原(20:00)\n",
    "三": "世界首领：少林·乱世，七秀·乱世(20:00)\n",
    "四": "阵营攻防：逐鹿中原(20:00)\n",
    "五": "世界首领：黑山林海，藏剑·乱世(20:00)\n",
    "六": "攻防前置：南屏山(12:00)\n阵营攻防：浩气盟；奇袭：恶人谷(13:00，19:00)\n",
    "日": "攻防前置：昆仑(12:00)\n阵营攻防：恶人谷；奇袭：浩气盟(13:00，19:00)\n"
}
'''日常任务对应表'''


@dataclass
class APP(object):
    '''jx3api的app类，关联url和cd时间'''
    url: str
    '''app的url'''
    cd: int
    '''app的cd时间'''


class JX3APP(Enum):
    '''jx3api的接口枚举'''
    日常任务 = APP("/app/daily", 0)
    开服检查 = APP("/app/check", 0)
    金价比例 = APP("/app/demon", 0)
    沙盘图片 = APP("/app/sand", 0)
    家园鲜花 = APP("/app/flower", 0)
    科举答题 = APP("/app/exam", 0)
    家园家具 = APP("/app/furniture", 0)
    查器物谱 = APP("/app/travel", 0)
    推荐小药 = APP("/app/heighten", 0)
    推荐装备 = APP("/app/equip", 0)
    推荐奇穴 = APP("/app/qixue", 0)
    查宏命令 = APP("/app/macro", 0)
    官方资讯 = APP("/app/news", 0)
    维护公告 = APP("/app/announce", 0)
    阵眼效果 = APP("/app/matrix", 0)
    物品价格 = APP("/app/price", 0)
    刷新地点 = APP("/app/horse", 0)
    主从大区 = APP("/app/server", 0)
    随机骚话 = APP("/app/random", 0)
    奇遇前置 = APP("/app/require", 0)
    免费奇遇攻略 = APP("/app/strategy", 0)
    付费奇遇攻略 = APP("/next/strategy", 0)
    奇遇查询 = APP("/next/serendipity", 10)
    奇遇统计 = APP("/next/statistical", 10)
    奇遇汇总 = APP("/next/collect", 10)
    资历排行 = APP("/next/seniority", 0)
    比赛战绩 = APP("/next/match", 10)
    战绩排行 = APP("/next/awesome", 10)
    战绩统计 = APP("/next/schools", 10)
    角色信息 = APP("/role/roleInfo", 0)
    装备属性 = APP("/role/attribute", 10)
    烟花记录 = APP("/role/secret", 10)

    加密计算 = APP("/token/calculate", 0)
    查有效值 = APP("/token/ticket", 0)
    到期查询 = APP("/token/socket", 0)
