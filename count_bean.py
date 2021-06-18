import requests
import json
import jdCookie
import re
from datetime import datetime, timedelta
import notification

"""
"""


def totalBean(cookies):
    headers = {
        'Host': 'wq.jd.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://wqs.jd.com/my/jingdou/my.shtml?sceneval=2',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('sceneid', '80027'),
        ('sceneval', '2'),
        ('callback', 'getUserInfoCb'),
    )

    response = requests.get('https://wq.jd.com/user/info/QueryJDUserInfo',
                            headers=headers, params=params, cookies=cookies)
    result = response.text
    regex = r"\"jdNum\" : (\d+)"
    matches = re.findall(regex, result, re.MULTILINE)
    if matches:
        return matches[0]
    return None


def jingDetailList(cookies, page):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://bean.m.jd.com',
        'Host': 'bean.m.jd.com',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Referer': 'https://bean.m.jd.com/beanDetail/index.action?resourceValue=bean',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {'page': str(page)}
    response = requests.post('https://bean.m.jd.com/beanDetail/detail.json',
                             headers=headers, cookies=cookies, data=data)
    result = response.json()
    if not result:
        return []
    beanList = result["jingDetailList"]
    return beanList

def qianDao(cookies):
    headers1 = {
     'Host': 'api.m.jd.com',
     'Connection': 'keep-alive',
     'User-Agent':'okhttp/3.12.1',
     'Accept-Language': 'zh-CN,en-US;q=0.9',
     'Accept-Encoding': 'gzip, deflate, br',
     'Content-Type':'application/x-www-form-urlencoded',
     'Charset':'UTF-8',
    }

    params = (
        ('functionId', 'signBeanAct'),
    )

    data =  {
        'body':'{"eid":"eidA967081212ascT40f7ANpSG+7HGB2vb4KXE+NIVnCZzPwc1VqaBwRbvuYUGhk9hFdP0tp5/I6uFKvyHo+y5S7JW5Uvi7+UX7Doe0t2vqtpoF0AElK","fp":"-1","jda":"-1","referUrl":"-1","rnVersion":"4.7","shshshfp":"-1","shshshfpa":"-1","userAgent":"-1"}',
    }

    addr='https://api.m.jd.com/client.action'
    addr='https://api.m.jd.com/client.action?functionId=signBeanAct&clientVersion=9.4.2&build=86916&client=android&d_brand=HUAWEI&d_model=STF-AL10&osVersion=9&screen=1920*1080&partner=huawei&oaid=bd33b7ff-f4ff-e77b-fe57-d6f95b6f95e7&eid=eidA967081212ascT40f7ANpSG+7HGB2vb4KXE+NIVnCZzPwc1VqaBwRbvuYUGhk9hFdP0tp5/I6uFKvyHo+y5S7JW5Uvi7+UX7Doe0t2vqtpoF0AElK&sdkVersion=28&lang=zh_CN&uuid=4587b4d704588eeb&aid=4587b4d704588eeb&area=12_904_905_50601&networkType=wifi&wifiBssid=unknown&uts=0f31TVRjBSsqndu4%2FjgUPz6uymy50MQJt%2FT2pfWlOS4ircGe9uXj5weXTGRI%2FLoLNhcw3asGSPBfTtSo%2F0C3zusSraijfol%2F6pFKN9T2ylO82uv%2Fev6uppuhFfyp78w6Kc8x4LRC7mCtk19fXpM1phWdkyY%2B4xDv%2B1sTlAQkwJxtPV2uIwlEryx8sCl50607YhoivmWZ0lCB5TAzcUM6hw%3D%3D&st=1615187312325&sign=f5f52526e712fbdd02dd5f5c6eca6020&sv=101'
    response = requests.post(addr,headers=headers1, data=data,cookies=cookies, params=params,verify=False)
    try:
        result = response.json()
        data = result["data"]
    except Exception as e:
        print(e)
        print(response.text)
        return None, None
    result =  response.text
    print(result)
    #print(json.loads(result))
    #print(result['dailyAward'])

def countTodayBean(cookies, _datatime):
    income = 0
    expense = 0
    page_1 = jingDetailList(cookies, 1)
    todayBeanList = [int(i["amount"])
                     for i in page_1 if _datatime in i["date"]]
    income_tmp = [i for i in todayBeanList if i > 0]
    expense_tmp = [i for i in todayBeanList if i < 0]
    income += sum(income_tmp)
    expense += sum(expense_tmp)
    page = 1
    while(len(page_1) == len(todayBeanList)):
        page += 1
        page_1 = jingDetailList(cookies, page)
        todayBeanList = [int(i["amount"])
                         for i in page_1 if _datatime in i["date"]]
        income_tmp = [i for i in todayBeanList if i > 0]
        expense_tmp = [i for i in todayBeanList if i < 0]
        income += sum(income_tmp)
        expense += sum(expense_tmp)
    return income, expense

def red(cookies):
    headers = {
        'Host': 'wq.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://wqs.jd.com/my/redpacket.shtml',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    params = (
        ('channel', '3'),
        ('type', '1'),
        ('page', '0'),
        ('pageSize', '100'),
        ('orgFlag', 'JD_PinGou_New'),
        ('expiredRedFlag', '1'),
        ('sceneval', '2'),
        ('g_login_type', '1'),
        ('g_ty', 'ls'),
    )

    response = requests.get('https://wq.jd.com/user/info/QueryUserRedEnvelopes',
                            headers=headers, params=params, cookies=cookies)
    try:
        result = response.json()
        data = result["data"]
    except:
        print("aaa")
        return None, None
    balance = data["balance"]
    expiredBalance = data["expiredBalance"] or 0
    return balance, expiredBalance


def miaoshaqiandao(cookies):
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Origin': 'https://h5.m.jd.com',
        'User-Agent': 'jdapp;android;9.4.2;9;8363731383030333136353136383-23D2534326132313536653035373;network/wifi;model/STF-AL10;addressid/137740131;aid/4587b4d704588eeb;oaid/bd33b7ff-f4ff-e77b-fe57-d6f95b6f95e7;osVer/28;appBuild/86916;partner/huawei;eufv/1;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 9; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044942 Mobile Safari/537.36',
        # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,en-US;q=0.9',
        'Referer':'https://h5.m.jd.com/babelDiy/Zeus/2NUvze9e1uWf4amBhe1AV6ynmSuH/index.html?sid=8f1b25b586373ac2ed2abf10deb0d37w&un_area=12_904_905_50601',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'com.jingdong.app.mall'
    }

    params = (
        ('sceneid', '80027'),
        ('sceneval', '2'),
        # ('g_login_type', '1'),
        ('callback', 'getUserInfoCb'),
        # ('g_ty', 'ls'),
    )
    data = {'functionId': 'doInteractiveAssignment',
            'client': 'wh5',
            'appid': 'SecKill2020',
            'body':'{"encryptProjectId":"4Rxa9S9Vcgmq5zVtPJzNdFwpzsar","encryptAssignmentId":"VegzgtziMHuipQLoycDf1Toe4jr","completionFlag":true,"actionType":0,"sourceCode":"aceacehttp1595403084552","ext":{"platform":"1","eid":"eidA967081212ascT40f7ANpSG+7HGB2vb4KXE+NIVnCZzPwc1VqaBwRbvuYUGhk9hFdP0tp5/I6uFKvyHo+y5S7JW5Uvi7+UX7Doe0t2vqtpoF0AElK","referUrl":"","userAgent":"jdapp;android;9.4.4;9;8363731383030333136353136383-23d2534326132313536653035373;network/wifi;model/stf-al10;addressid/137740131;aid/4587b4d704588eeb;oaid/bd33b7ff-f4ff-e77b-fe57-d6f95b6f95e7;osver/28;appbuild/87076;partner/huawei;eufv/1;jdsupportdarkmode/0;mozilla/5.0 (linux; android 9; stf-al10 build/huaweistf-al10; wv) applewebkit/537.36 (khtml, like gecko) version/4.0 chrome/66.0.3359.126 mqqbrowser/6.2 tbs/044942 mobile safari/537.36"}}',
            }
    response = requests.post('https://api.m.jd.com/client.action', headers=headers, cookies=cookies, data=data, verify=False)
    result = response.text
    print(result)

def zhuanpan_3times(cookies):
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Origin': 'https://h5.m.jd.com',
        'User-Agent': 'jdapp;android;9.4.2;9;8363731383030333136353136383-23D2534326132313536653035373;network/wifi;model/STF-AL10;addressid/137740131;aid/4587b4d704588eeb;oaid/bd33b7ff-f4ff-e77b-fe57-d6f95b6f95e7;osVer/28;appBuild/86916;partner/huawei;eufv/1;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 9; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044942 Mobile Safari/537.36',
        # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-CN,en-US;q=0.9',
        'Referer':'https://h5.m.jd.com/babelDiy/Zeus/yj8mbcm6roENn7qhNdhiekyeqtd/index.html?sid=8f1b25b586373ac2ed2abf10deb0d37w&un_area=12_904_905_50601',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'com.jingdong.app.mall',
        'Content-Type':'text/plain'
    }

    params = (
        ('functionId','getLuckDrawEntrance'),
        ('body', '%7B%22platformType%22%3A%221%22%7D'),
        ('appid', 'couponPackDetail'),
        ('client','m'),
        ('geo','%5Bobject%20Object%5D'),

    )
    data = {'functionId': 'doInteractiveAssignment',
            'client': 'wh5',
            'appid': 'SecKill2020',
            'body':'{"encryptProjectId":"4Rxa9S9Vcgmq5zVtPJzNdFwpzsar","encryptAssignmentId":"VegzgtziMHuipQLoycDf1Toe4jr","completionFlag":true,"actionType":0,"sourceCode":"aceacehttp1595403084552","ext":{"platform":"1","eid":"eidA967081212ascT40f7ANpSG+7HGB2vb4KXE+NIVnCZzPwc1VqaBwRbvuYUGhk9hFdP0tp5/I6uFKvyHo+y5S7JW5Uvi7+UX7Doe0t2vqtpoF0AElK","referUrl":"","userAgent":"jdapp;android;9.4.4;9;8363731383030333136353136383-23d2534326132313536653035373;network/wifi;model/stf-al10;addressid/137740131;aid/4587b4d704588eeb;oaid/bd33b7ff-f4ff-e77b-fe57-d6f95b6f95e7;osver/28;appbuild/87076;partner/huawei;eufv/1;jdsupportdarkmode/0;mozilla/5.0 (linux; android 9; stf-al10 build/huaweistf-al10; wv) applewebkit/537.36 (khtml, like gecko) version/4.0 chrome/66.0.3359.126 mqqbrowser/6.2 tbs/044942 mobile safari/537.36"}}',
            }
    addr='https://api.m.jd.com/client.action?functionId=getLuckDrawEntrance&body=%7B%22platformType%22%3A%221%22%7D&appid=couponPackDetail&client=m&clientVersion=1.0.0&area=12_904_905_50601&geo=%5Bobject%20Object%5D&eu=8363731383030333136353136383&fv=23D2534326132313536653035373'
    response = requests.post(addr, headers=headers, cookies=cookies,  verify=False)
    result = response.text
    print(result)

    print("second time")
    response = requests.post(addr, headers=headers, cookies=cookies, verify=False)
    result = response.text
    print(result)

    #time.leep(1)
    print("third time")
    response = requests.post(addr, headers=headers, cookies=cookies, verify=False)
    result = response.text
    print(result)

def jd_tiantiansignnew(cookies):
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'Keep-Alive',
        'Origin': 'https://h5.m.jd.com',
        'User-Agent':'okhttp/3.12.1',
        'Accept-Language': 'zh-CN,en-US;q=0.9',
        'Referer':'https://h5.m.jd.com/babelDiy/Zeus/yj8mbcm6roENn7qhNdhiekyeqtd/index.html?sid=8f1b25b586373ac2ed2abf10deb0d37w&un_area=12_904_905_50601',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'com.jingdong.app.mall',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
    }

    params = (
        ('functionId','ccSignInNew'),
        ('body', '%7B%22platformType%22%3A%221%22%7D'),
        ('appid', 'couponPackDetail'),
        ('client','m'),
        ('geo','%5Bobject%20Object%5D'),

    )
    data = {
            'body': '{"childActivityUrl":"openapp.jdmobile://virtual?params={\\"category\\":\\"jump\\",\\"des\\":\\"couponCenter\\"}","eid":"eidA967081212ascT40f7ANpSG+7HGB2vb4KXE+NIVnCZzPwc1VqaBwRbvuYUGhk9hFdP0tp5/I6uFKvyHo+y5S7JW5Uvi7+UX7Doe0t2vqtpoF0AElK","monitorRefer":"appClient","monitorSource":"cc_sign_android_index_config","pageClickKey":"Coupons_GetCenter","pin":"281f08a7768fd3326e82a93ceef73104","sessionId":"","shshshfpb":"tanCuOqNJGuM2rMyUfN488yD7pacn00MAJvcSMP67YqExqlHbANspbdX9wLeRmvZV/vaQty+edb/C2t8zXMeb57yw2juUzgNbplcdYz+V8NQ=","verifyToken":""}',
            }
    addr='https://api.m.jd.com/client.action?functionId=ccSignInNew&clientVersion=9.4.4&build=87076&client=android&d_brand=HUAWEI&d_model=STF-AL10&osVersion=9&screen=1920*1080&partner=huawei&oaid=bd33b7ff-f4ff-e77b-fe57-d6f95b6f95e7&eid=eidA967081212ascT40f7ANpSG+7HGB2vb4KXE+NIVnCZzPwc1VqaBwRbvuYUGhk9hFdP0tp5/I6uFKvyHo+y5S7JW5Uvi7+UX7Doe0t2vqtpoF0AElK&sdkVersion=28&lang=zh_CN&uuid=4587b4d704588eeb&aid=4587b4d704588eeb&area=12_904_905_50601&networkType=wifi&wifiBssid=unknown&uts=0f31TVRjBSsqndu4%2FjgUPz6uymy50MQJNEcBBqXs8flvr8dIWOoeJ55S0bN9%2FowQ5%2FPQF3Lh3InX6ifpD1A%2Fq2ZCD%2BGcdWb7NtdW7RrssdXIJPPUs%2FuplMnMP8%2Fms0ibvpx%2FPbe9TpImri7SwSyadU7TiBoeFnF7lilEZtTeZkMmxBlMrtH%2FzYwKasNxtDxN7WJlfPIB92edIk6kwQzKHQ%3D%3D&st=1615441254230&sign=e708355ab2c517596d6b4eafddab28f1&sv=121'
    response = requests.post(addr, headers=headers, cookies=cookies,data=data,  verify=False)
    result = response.text
    print(result)

def run():
    utc_dt = datetime.utcnow()  
    bj_dt = utc_dt+timedelta(hours=8)  
    _datatime = bj_dt.strftime("%Y-%m-%d", )
    now = bj_dt.strftime("%Y-%m-%d %H:%M:%S")
    message = ""
    for cookies in jdCookie.get_cookies():
        print(f"""[ {cookies["pt_pin"]} ]""")
        jd_tiantiansignnew(cookies)
        zhuanpan_3times(cookies)
        qianDao(cookies)
        miaoshaqiandao(cookies)
        total = totalBean(cookies)
        balance, expiredBalance = red(cookies)
        income, expense = countTodayBean(cookies, _datatime)
        message += f'\n\n【{cookies["pt_pin"]}】 \n当前京豆: {total} \n今日收入: {income} \n今日支出: {expense}\n红包合计: {balance}元 \n即将过期: {expiredBalance}元'
        print("\n")
    print(f"⏰ 京豆统计 {now}")
    message += "\n\n\n[注] 即将过期指 过了零点就会失效"
    print(message)
    notification.notify(f"⏰ 京豆统计 {now}", message)


if __name__ == "__main__":
    run()
