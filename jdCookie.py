import requests
import json
import time
import os
import re
import notification

"""
1、抓包，登录 https://bean.m.jd.com 点击签到并且出现签到日历后
2、返回抓包，搜索关键词 functionId=signBean 复制Cookie中的pt_key与pt_pin
       电脑获取cookie可以参考 https://ruicky.me/2020/07/18/jd-cookie/
3、注意，cookies会过期,大约为一个月
4、python3.6+ 环境，需要requests包
集中cookie管理
多账号准备
过期检查
需要推送通知的，修改notification.py
"""

###############################
# 方案1 本地执行、云服务器、云函数等等   下载到本地，填写参数，执行

cookies1 = {
    'pt_key': 'AAJgQMPwADAI3BuizFse3tw6D0Fy_cl2_x27kW_LoLoRWM8H5vmwOPHCCabVXewaQNL944pbjWE',  # cookie参数填写，填写完注意不要上传
    'pt_pin': 'proing2007',
}
cookiesk = {
    'pt_key': 'AAJgQL9IADAKREsxTrkJmRcUMApkp5L7K0ydm7u22hcK_bt_bgaUQzvJ3gMsGbPirdxpDABiFxg',  # cookie参数填写，填写完注意不要上传
    'pt_pin': 'jd_75ea496eaaff9',
}

cookiescp = {
    'pt_key': 'AAJgQYm2ADAKimx8ggkwB945sQTmmRkAHpXs2JNg9kXxHInLApqW-ncDLk59ENbbFzzegKp_IBk',
    'pt_pin': 'cp1573',
}
cookiesk1 = {
    'pt_key': 'AAJgTsCIADC8lhhb4-HwMLPpycb0neUY8Jr9UtBGy_pZuww7sCoEpI_ZKpRnCq8APfQTh8oh0Yw',
    'pt_pin': 'jd_DsBxsOPefLwi',
}
cookiesJ = {
    'pt_key': 'AAJgUfGIADB6pHVuCpIq9viaSn8PlPIB2Yx9dSTMY5Wx8lTu7DMyu0Sh93TtZwJifyE4hmy2Uzg',
    'pt_pin': 'jd_62b22b61e73e3',
}
cookies6 = {
    'pt_key': 'AAJgTyAJADCiEz1jsxZyOPSQgsJ23U3Pjh1Pyk8OtIraA8y14JHVsPQdn8ypToYIgNJ5-n1hrQc',
    'pt_pin': 'jd_4195ba6d85400',
}



cookiesLists = [cookies1,cookiesk,cookiescp,cookiesk1,cookiesJ,cookies6]


####################################
# 方案2 GitHub action 自动运行    cookies读取自secrets  
if "JD_COOKIE1" in os.environ:
    """
    判断是否运行自 GitHub action, "JD_COOKIE" 该参数与 repo里的Secrets的名称保持一致
    """
    print("执行自GitHub action")
    secret = os.environ["JD_COOKIE"]
    cookiesLists = []  # 重置cookiesList
    for line in secret.split('\n'):
        pt_pin = re.findall(r'pt_pin=(.*?)&', line)[0]
        pt_key = re.findall(r'pt_key=(.*?)$', line)[0]
        cookiesLists.append({"pt_pin": pt_pin, "pt_key": pt_key})

#######################################



def valid(cookies):
    headers = {
        'Host': 'api.m.jd.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'jdapp;iPhone;8.5.5;13.5;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = (
        ('functionId', 'plantBeanIndex'),
        ('body', json.dumps(
            {"monitor_source": "plant_m_plant_index", "version": "8.4.0.0"})),
        ('appid', 'ld'),
    )
    response = requests.get('https://api.m.jd.com/client.action',
                            headers=headers, params=params, cookies=cookies)
    if response.json()["code"] == "3":
        print(f"""## {cookies["pt_pin"]}: cookie过期""")
        notification.notify(
            f"""## 京东账号【{cookies["pt_pin"]}】 cookie过期""", f"""## 账号【{cookies["pt_pin"]}】 cookie过期 ，及时修改""")
        return False
    return True


def get_cookies():
    return [i for i in cookiesLists if valid(i)]


print("***"*20)
print("***"*20)
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

if __name__ == "__main__":
    print(">>>检查有效性")
    for i in get_cookies():
        print(i)
