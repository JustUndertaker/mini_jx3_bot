from httpx import AsyncClient
from pydantic import BaseModel

from src.config import Jx3ApiConfig

class Response(BaseModel):
    """返回数据模型"""

    code: int
    """状态码"""
    msg: str
    """返回消息字符串"""
    data: dict | list[dict]
    """返回数据"""
    time: int
    """时间戳"""

class JX3API:
    """jx3api接口类"""

    client: AsyncClient
    """浏览器客户端"""
    config: Jx3ApiConfig
    """api设置"""

    async def app_daily(self, *, server: str, next: int = ...) -> Response:
        """
        说明：
            今天、明天、后天等的日常任务，七点自动更新。

        参数：
            * `server`：服务器名
            * `next`: 可选，查询天数，默认为0
        """
        ...
    async def app_calculate(self, *, count: int = ...) -> Response:
        """
        说明:
            搜索当天前后指定日期的日常信息

        参数:
            * `count`：可选，计算天数，搜索当天前后指定日期的日常信息
        """
        ...
    async def app_check(self, *, server: str) -> Response:
        """
        说明：
            检查目标服务器的开服状态，可用于开服监控。

        参数：
            * `server`：服务器名
        """
        ...
    async def app_status(self, *, server: str) -> Response:
        """
        说明:
            检查指定区服的状态，不适用于开服监控

        参数:
            * `server`：服务器名
        """
        ...
    async def app_demon(self, *, server: str) -> Response:
        """
        说明：
            检查近十天的金价比例，数据仅供参考。

        参数:
            * `server`：服务器名
        """
        ...
    async def app_exam(self, *, question: str) -> Response:
        """
        说明:
            搜索科举题目的答案，支持首字母，支持模糊搜索。

        参数:
            * `question`：科举题目，搜索目标题目答案
        """
        ...
    async def app_flower(
        self, *, server: str, map: str = ..., flower: str = ...
    ) -> Response:
        """
        说明:
            检查当天鲜花最高价格收购线路。

        参数:
            * `server`：服务器名
            * `map`：可选，用于筛选地图
            * `flower`：可选， 用于筛选鲜花
        """
        ...
    async def app_furniture(self, *, name: str) -> Response:
        """
        说明:
            家园家具信息

        参数:
            * `name`：家具名称
        """
        ...
    async def app_travel(self, *, name: str) -> Response:
        """
        说明:
            搜索地图产出的详细家具属性。

        参数:
            * `name`：地图名称，搜索产出家具详细属性，不支持模糊搜索
        """
        ...
    async def app_heighten(self, *, name: str) -> Response:
        """
        说明:
            推荐当前赛季所使用的小吃小药。

        参数:
            * `name`：心法名称
        """
        ...
    async def app_equip(self, *, name: str) -> Response:
        """
        说明:
            推荐当前赛季所使用的装备。

        参数:
            * `name`：心法名称
        """
        ...
    async def app_macro(self, *, name: str) -> Response:
        """
        说明:
            推荐当前赛季热门的宏命令。

        参数:
            * `name`：心法名称
        """
        ...
    async def app_news(self, *, limit: int = ...) -> Response:
        """
        说明:
            搜索官方近期发布的最新公告，新闻等相关内容。

        参数:
            * `limit`：可选，限制返回数量，可选范围1-50，默认10
        """
        ...
    async def app_announce(self, *, limit: int = ...) -> Response:
        """
        说明:
            搜索官方近期发布的维护公告。

        参数:
            * `limit`：可选，限制返回数量，可选范围1-50，默认10
        """
        ...
    async def app_matrix(self, *, name: str) -> Response:
        """
        说明:
            搜索心法阵眼效果

        参数:
            * `name`：心法名称
        """
        ...
    async def app_price(self, *, name: str) -> Response:
        """
        说明:
            搜索黑市的外观物品最新价格。

        参数:
            * `name`：物品名称
        """
        ...
    async def app_horse(self, *, name: str) -> Response:
        """
        说明:
            搜索某个地图刷新的马驹名称和刷新位置。

        参数:
            * `name`：地图名称/马驹名称
        """
        ...
    async def app_server(self, *, name: str) -> Response:
        """
        说明:
            主从大区

        参数:
            * `name`：大区名称
        """
        ...
    async def app_random(self) -> Response:
        """
        说明:
            召唤一条骚话。
        """
        ...
    async def app_require(self, *, name: str) -> Response:
        """
        说明:
            搜索目标奇遇的前置要求。

        参数:
            * `name`：奇遇名称
        """
        ...
    async def app_strategy(self, *, name: str) -> Response:
        """
        说明:
            搜索某个奇遇的任务攻略，不需要token

        参数:
            * `name`：奇遇名称
        """
        ...
    async def next_price(self, *, name: str) -> Response:
        """
        说明:
            搜索外观物品最新价格，统计了各个来源的数据，补充了更多的关键字。

        参数:
            * `name`： 外观简称
        """
        ...
    async def next_strategy(self, *, name: str) -> Response:
        """
        说明:
            搜索某个奇遇的任务攻略。

        参数:
            * `name`：奇遇名称
        """
        ...
    async def next_serendipity(
        self, *, server: str, name: str, ticket: str
    ) -> Response:
        """
        说明:
            搜索某个角色触发的所有奇遇记录。

        参数:
            * `server`：服务器名
            * `name`：角色名
            * `ticket`：推栏app的ticket
        """
        ...
    async def next_statistical(
        self, *, server: str, serendipity: str = ..., limit: int = ...
    ) -> Response:
        """
        说明:
            搜索某个奇遇最近触发人。

        参数:
            * `server`：服务器名
            * `serendipity`：可选，奇遇名，默认空（返回全部奇遇）
            * `limit`：可选，返回条目，支持1-50，默认20
        """
        ...
    async def next_collect(self, *, server: str, days: int = ...) -> Response:
        """
        说明:
            统计指定时间内触发次数和最后触发人。

        参数:
            * `server`：服务器名
            * `days`：可选，指定统计天数的触发次数，默认值7（统计七天内的记录）
        """
        ...
    async def server_serendipity(self, *, serendipity: str) -> Response:
        """
        说明:
            查询全服的指定奇遇数据。

        参数:
            * `serendipity`：奇遇名
        """
        ...
    async def server_statistical(
        self, *, serendipity: str, limit: int = ...
    ) -> Response:
        """
        说明:
            统计全服的指定奇遇触发记录。

        参数:
            * `serndipity`：奇遇名
            * `limit`：可选，返回条目，支持1-50，默认20
        """
        ...
    async def next_fall(self, *, server: str, name: str) -> Response:
        """
        说明:
            查询特殊物品掉落情况

        参数:
            * `server`：服务器名
            * `name`：特殊物品名称，如天乙玄晶
        """
        ...
    async def next_sum(self, *, server: str) -> Response:
        """
        说明:
            统计服务器掉落物品

        参数:
            * `server`：服务器名
        """
        ...
    async def next_seniority(
        self, *, server: str, ticket: str, kungfu: str = ...
    ) -> Response:
        """
        说明:
            搜索某个门派的资历排行榜。

        参数:
            * `server`：服务器名
            * `ticket`：推栏app的ticket
            * `kungfu`：可选，输入指定门派缩写（如：万花、七秀），默认值ALL（返回全门派）
        """
        ...
    async def next_arena(
        self, *, server: str, name: str, ticket: str, match: int = ...
    ) -> Response:
        """
        说明:
            搜索某个角色的战绩评分和近期战斗记录。

        参数:
            * `server`：服务器名
            * `name`：角色名
            * `ticket`：推栏app的ticket
            * `match`：可选，比赛模式，可选值22/33/55，未输入或输入0 时返回全部模式记录。
        """
        ...
    async def next_awesome(self, *, ticket: str, match: int = ...) -> Response:
        """
        说明:
            搜索某个比赛模式的战绩排名记录。

        参数:
            * `ticket`：推栏app的ticket
            * `match`：可选，比赛模式，可选值22/33/55，默认值33。
        """
        ...
    async def next_schools(self, *, ticket: str, match: int = ...) -> Response:
        """
        说明:
            搜索某个比赛模式的门派排名统计。

        参数:
            * `ticket`：推栏app的ticket
            * `match`：比赛模式，可选值22/33/55，默认值33。
        """
        ...
    async def role_roleInfo(self, *, server: str, name: str) -> Response:
        """
        说明:
            搜索某个角色的信息。

        参数:
            * `server`：服务器名
            * `name`：角色名
        """
        ...
    async def role_attribute(self, *, server: str, name: str, ticket: str) -> Response:
        """
        说明:
            搜索某个角色的装备和属性。

        参数:
            * `server`：服务器名
            * `name`：角色名
            * `ticket`：推栏app的ticket
        """
        ...
    async def role_firework(self, *, server: str, name: str) -> Response:
        """
        说明:
            搜索某个角色的烟花赠送或接收记录。

        参数:
            * `server`：服务器名
            * `name`：角色名
        """
        ...
    async def transmit_chat(
        self, *, secretId: str, secretKey: str, name: str, question: str
    ) -> Response:
        """
        说明:
            腾讯云智能闲聊（NLP），不是SDK版本。

        参数:
            * `secretId`：腾讯云secretId
            * `secretKey`：腾讯云secretKey
            * `name`：机器人名称
            * `question`：对话内容
        """
        ...
    async def transmit_alitts(
        self,
        *,
        appkey: str,
        access: str,
        secret: str,
        voice: str,
        format: str,
        sample_rate: int,
        volume: int,
        speech_rate: int,
        pitch_rate: int,
        text: str
    ) -> Response:
        """
        说明:
            阿里云语音合成（TTS），不是SDK版本。

        参数:
            * `appkey`：阿里云appkey
            * `access`：阿里云access
            * `secret`：阿里云secret
            * `voice`：发音人，默认Aitong
            * `format`：编码格式，支持 PCM WAV MP3，默认：MP3
            * `sample_rate`：采样率，默认：16000
            * `volume`：音量，取值范围：0～100，默认：50
            * `speech_rate`：语速，取值范围：-500～500，默认：0
            * `pitch_rate`： 音调，取值范围：-500～500，默认：0
        """
        ...
    async def transmit_idiom(self, *, word: str) -> Response:
        """
        说明:
            搜索下一个成语，已清除收尾同音的成语。

        参数:
            * `word`：输入四字成语，已去除收尾同音成语。
        """
        ...
    async def transmit_random(self) -> Response:
        """
        说明:
            召唤一条舔狗日志。
        """
        ...
    async def cloud_demon(self, *, server: str, robot: str = ...) -> Response:
        """
        说明:
            图片api，检查近十天的金价比例，数据仅供参考。

        参数:
            * `server`：服务器名
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_flower(
        self, *, server: str, flower: str, robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，检查当天鲜花最高价格收购线路。

        参数:
            * `server`：服务器名
            * `flower`：鲜花名
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_price(self, *, name: str, robot: str = ...) -> Response:
        """
        说明:
            图片api，搜索黑市的外观物品最新价格。

        参数:
            * `name`：物品/外观名称
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_serendipity(
        self, *, server: str, name: str, ticket: str, robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，搜索某个角色触发的所有奇遇记录。

        参数:
            * `server`：服务器名
            * `name`：角色名
            * `ticket`：推栏app的ticket
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_statistical(
        self, *, serendipity: str, robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，搜索某个奇遇最近触发人。

        参数:
            * `serendipity`：服务器名
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_collect(self, *, server: str, robot: str = ...) -> Response:
        """
        说明:
            图片api，统计指定时间内触发次数和最后触发人。

        参数:
            * `server`：服务器名
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_seniority(
        self, *, server: str, ticket: str, kungfu: str = ..., robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，搜索某个门派的资历排行榜。

        参数:
            * `server`：服务器名
            * `ticket`：推栏app的ticket
            * `kungfu`：可选，门派缩写（如：万花、七秀）默认值ALL
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_attribute(
        self, *, server: str, name: str, ticket: str, robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，搜索某个角色的装备和属性。

        参数:
            * `server`：服务器名
            * `name`：角色名
            * `ticket`：推栏app的ticket
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_arena(
        self, *, server: str, name: str, ticket: str, match: int = ..., robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，搜索某个角色的战绩评分和近期战斗记录。

        参数:
            * `server`：服务器名
            * `name`：角色名
            * `ticket`：推栏app的ticket
            * `match`：可选，比赛模式，可选值22/33/55，未输入或输入0 时返回全部模式记录
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_awesome(
        self, *, ticket: str, match: int = ..., robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，搜索某个比赛模式的战绩排名记录。

        参数:
            * `ticket`：推栏app的ticket
            * `match`：可选，比赛模式，可选值22/33/55，默认值33
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_schools(
        self, *, ticket: str, match: int = ..., robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，搜索某个比赛模式的门派排名统计。

        参数：
            * `ticket`：推栏app的ticket
            * `match`：可选，比赛模式，可选值22/33/55，默认值33
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_server_demon(self, *, robot: str = ...) -> Response:
        """
        说明:
            图片api，统计全服的金价数据。

        参数:
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_calculate(self, *, robot: str = ...) -> Response:
        """
        说明:
            图片api，推算前后十五天的日常。

        参数:
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_server_statistical(
        self, *, serendipity: str, robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，统计全服的奇遇数据。

        参数:
            * `serendipity`：奇遇名
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_server_serendipity(
        self, *, serendipity: str, robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，查询全服的奇遇数据。

        参数:
            * `serendipity`：奇遇名
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_fall(self, *, server: str, name: str, robot: str = ...) -> Response:
        """
        说明:
            图片api，统计服务器物品掉落

        参数:
            * `server`：服务器名
            * `name`：道具名
        """
        ...
    async def cloud_sum(self, *, server: str, robot: str = ...) -> Response:
        """
        说明:
            图片api，汇总服务器特殊掉落

        参数:
            * `server`：服务器名
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_firework(
        self, *, server: str, name: str, robot: str = ...
    ) -> Response:
        """
        说明:
            图片api，查询指定玩家的烟花燃放记录。

        参数:
            * `server`：服务器名
            * `name`：玩家名
            * `robot`：可选，用于自定义水印
        """
        ...
    async def cloud_circles(self, *, url: str = ..., text: str = ...) -> Response:
        """
        说明:
            图片api，合成一张水墨圈圈的图片。

        参数:
            * `url`： 可选，图片链接，可以传入QQ号或者完整的URL,传入URL需要注意URL自身的拼接符
            * `text`：可选，需要合成的字符串，建议输入角色名称
        """
        ...
    async def token_calculate(
        self,
        *,
        cursor: int,
        size: int,
        gameVersion: int,
        zoneName: str,
        serverName: str,
        forceId: int,
        ts: str
    ) -> Response:
        """
        说明:
            对推栏的请求加密计算。

        参数:
            略
        """
        ...
    async def token_ticket(self, *, ticket: str) -> Response:
        """
        说明:
            查询ticket的可用性。

        参数:
            * `ticket`：推栏app的ticket
        """
        ...
    async def token_socket(self, *, token: str) -> Response:
        """
        说明:
            查询Ws Token的服务到期时间。

        参数:
            * `token`：ws token，不是api token
        """
        ...
