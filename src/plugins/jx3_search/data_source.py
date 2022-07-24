import time
from datetime import datetime

# -------------------------------------------------------------
# 返回数据处理阶段，处理api返回data，方便模板使用
# -------------------------------------------------------------


def handle_data_price(data: list[list[dict]]) -> dict:
    """处理物价数据"""
    req_data = {}
    for one_data in data:
        for one_item in one_data:
            zone = one_item["zone"]
            if zone not in req_data:
                req_data[zone] = []
            req_data[zone].append(one_item)
    return req_data


def handle_data_serendipity(data: list[dict]) -> list[dict]:
    """处理奇遇统计"""
    req_data = []
    for one_data in data:
        get_time: int = one_data["time"]
        if get_time == 0:
            time_str = "未知"
            day = "过去太久啦"
        else:
            time_now = datetime.now()
            time_pass = datetime.fromtimestamp(get_time)
            time_str = time_pass.strftime("%Y-%m-%d %H:%M:%S")
            day = f"{(time_now-time_pass).days} 天前"
        one_dict = {
            "time": time_str,
            "day": day,
            "serendipity": one_data["serendipity"],
        }
        req_data.append(one_dict)
    return req_data


def handle_data_serendipity_list(data: list[dict]) -> list[dict]:
    """处理奇遇统计数据"""
    req_data = []
    for one_data in data:
        get_time: int = one_data["time"]
        if get_time == 0:
            time_str = "未知"
            day = "过去太久啦"
        else:
            time_now = datetime.now()
            time_pass = datetime.fromtimestamp(get_time)
            time_str = time_pass.strftime("%Y-%m-%d %H:%M:%S")
            day = f"{(time_now-time_pass).days} 天前"
        one_dict = {"time": time_str, "day": day, "name": one_data["name"]}
        req_data.append(one_dict)
    return req_data


def handle_data_serendipity_summary(data: list[dict]) -> list[dict]:
    """处理奇遇汇总数据"""
    req_data = []
    for _data in data:
        one_data = _data["data"]
        get_time: int = one_data["time"]
        if get_time == 0:
            time_str = "未知"
            day = "过去太久啦"
        else:
            time_now = datetime.now()
            time_pass = datetime.fromtimestamp(get_time)
            time_str = time_pass.strftime("%Y-%m-%d %H:%M:%S")
            day = f"{(time_now-time_pass).days} 天前"
        one_dict = {
            "time": time_str,
            "day": day,
            "name": one_data["name"],
            "serendipity": _data["serendipity"],
        }
        req_data.append(one_dict)
    return req_data


def handle_data_match(data: dict) -> dict:
    """处理战绩数据"""
    req_data = {}
    req_data["performance"] = data["performance"]
    history: list = data["history"]
    req_data["history"] = []
    for one_data in history:
        one_req_data = {}
        one_req_data["kungfu"] = one_data["kungfu"]
        one_req_data["avgGrade"] = one_data["avgGrade"]
        one_req_data["won"] = one_data["won"]
        one_req_data["totalMmr"] = one_data["totalMmr"]
        one_req_data["mmr"] = abs(one_data["mmr"])

        pvp_type = one_data.get("pvpType")
        if pvp_type == 2:
            one_req_data["pvpType"] = "2v2"
        elif pvp_type == 3:
            one_req_data["pvpType"] = "3v3"
        else:
            one_req_data["pvpType"] = "5v5"
        start_time = one_data.get("startTime")
        end_time = one_data.get("endTime")
        time_keep = end_time - start_time
        pvp_time = int((time_keep + 30) / 60)
        if pvp_time == 0:
            pvp_time = 1
        one_req_data["time"] = str(pvp_time) + " 分钟"

        time_now = time.time()
        time_ago = time_now - end_time
        if time_ago < 3600:
            # 一小时内用分钟表示
            time_end = int((time_ago + 30) / 60)
            if time_end == 0:
                time_end = 1
            one_req_data["ago"] = str(time_end) + " 分钟前"
        elif time_ago < 86400:
            # 一天内用小时表示
            time_end = int((time_ago + 1800) / 3600)
            if time_end == 0:
                time_end = 1
            one_req_data["ago"] = str(time_end) + " 小时前"
        elif time_ago < 864000:
            # 10天内用天表示
            time_end = int((time_ago + 43200) / 86400)
            if time_end == 0:
                time_end = 1
            one_req_data["ago"] = str(time_end) + " 天前"
        else:
            # 超过10天用日期表示
            timeArray = time.localtime(end_time)
            one_req_data["ago"] = time.strftime("%Y年%m月%d日", timeArray)
        req_data["history"].append(one_req_data)
        req_data["camp"] = data.get("camp", "")
    return req_data


def handle_data_equip(data: dict) -> dict:
    """处理装备属性"""
    req_data = {}
    req_data["kungfu"] = data["kungfu"]
    req_data["dateTime"] = data["dateTime"]
    info = data["info"]
    if info:
        req_data["score"] = info.get("score")

        # 处理info数据
        info_panel: list[dict] = info["panel"]
        data_info = []
        for one in info_panel:
            value = str(one["value"])
            if one["percent"]:
                value += "%"
            one_data = {"name": one["name"], "value": value}
            data_info.append(one_data)
        req_data["info"] = data_info

    color_level_map = {
        "0": "darkgray",
        "1": "gray",
        "2": "darkgreen",
        "3": "dodgerblue",
        "4": "blueviolet",
        "5": "chocolate",
    }
    # 处理equip数据
    equip: list[dict] = data["equip"]
    data_equip = []
    for one in equip:
        _source = one.get("source")
        if _source is None:
            source = ""
        else:
            source = _source.split("；")[0]
        one_data = {
            "name": one["name"],
            "kind": one["subKind"],
            "icon": one["icon"],
            "quality": one["quality"],
            "color": color_level_map.get(one["color"], "black"),
            "strengthLevel": int(one["strengthLevel"]),
            "source": source,
        }
        # 五行石图标
        five_stone: list = one.get("fiveStone")
        if five_stone is not None:
            one_data["fiveStone"] = [i["icon"] for i in five_stone]
        # 属性描述
        modifyType: list = one.get("modifyType")
        if modifyType is not None:
            name_list = [i["name"] for i in modifyType]
            one_data["modifyType"] = " ".join(name_list)
        # 附魔描述
        permanentEnchant: list = one.get("permanentEnchant")
        if permanentEnchant is not None:
            name_list = [i["name"] for i in permanentEnchant]
            one_data["permanentEnchant"] = " ".join(name_list)
        else:
            one_data["permanentEnchant"] = ""
        data_equip.append(one_data)
    req_data["equip"] = data_equip

    # 处理qixue数据
    qixue: list = data["qixue"]
    data_qixue = []
    for one in qixue:
        if one["name"] == "未知":
            continue
        one_data = {
            "name": one["name"],
            "icon": one["icon"],
        }
        data_qixue.append(one_data)
    req_data["qixue"] = data_qixue

    return req_data
