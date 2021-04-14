import jdCookie
import json
import requests
import time


"""
1、此脚本用于东东农场 【好友】邀请助力 添加好友
2、效果:新加好友时为对方增加10g水;对方执行此脚本同理
3、此助力独立于助力得水，目前助力上限未知
4、欢迎补充一个足够多的shareCodes列表
5、cron 0 */3 * * *
"""
shareCodes = ["b183f834ec304af28567db5e2e492839",
              "d00ef6357f264550a50dff70204ddfdb",
              "7e568ac242934d6f856ebe8364a9828b",
              "1d502afa8d254418bbe36d34fb54c712",
              "c6ece1d270704bf6830db09165bdf757",
              "cd54168b2de34fbbb5d3b9e92ef3d78b",
              "b5ced0078d2c445484a98c4053382aca",
              "80fe97d7250548868ae9db9bec751055",
              ]  


def postTemplate(cookies, functionId, body):
    headers = {
        'User-Agent': 'JD4iPhone/167249 (iPhone; iOS 13.5.1; Scale/3.00)',
        'Host': 'api.m.jd.com',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    params = (
        ('functionId', functionId),
    )
    data = {
        'body': json.dumps(body),
        "appid": "wh5",
        "clientVersion": "9.1.0"
    }
    response = requests.post(
        'https://api.m.jd.com/client.action', headers=headers, cookies=cookies, data=data, params=params)
    return response.json()


def help(cookies):
    print("\n")
    data = postTemplate(cookies, "friendListInitForFarm",
                        {})

    print("他人运行此脚本为我助力")
    print(f"""今日新增好友: {data["inviteFriendCount"]}/10""")
    if data["inviteFriendCount"] > 0 and data["inviteFriendCount"] > data["inviteFriendGotAwardCount"]:
        print("领取邀请奖励")
        print(postTemplate(cookies, "awardInviteFriendForFarm", {}))
    print("\n>>>开始为他人助力")
    myFriendCode = [i["shareCode"]
                    for i in data["friends"] if "shareCode" in i]
    countOfFriend = data["countOfFriend"]
    _friendsList = [i for i in data["friends"]]
    if not _friendsList:
        print("好友列表为空  跳出")
        print(data)
        return
    lastId = _friendsList[-1]["id"]
    print(f"""fullFriend:{data["fullFriend"]}""")  # 好友添加总数有上限
    if data["fullFriend"]:
        print("好友达到上限,退出")
        return
    for i in range(countOfFriend//20):
        result = postTemplate(cookies, "friendListInitForFarm",
                              {"lastId": lastId})
        pageFriend = [i["shareCode"] for i in result["friends"]]
        if not result["friends"]:
            break

        lastId = [i for i in result["friends"]][-1]["id"]
        myFriendCode += pageFriend
    myshareCode = postTemplate(cookies, 'initForFarm', {})[
        "farmUserPro"]["shareCode"]

    shareCodes_diff = list(
        set(shareCodes).difference(myFriendCode, [myshareCode]))  # 去掉自己以及已是好友关系的shareCode
    print("准备助力的shareCodes:", shareCodes_diff)
    if not shareCodes_diff:
        print("脚本中的shareCodes暂时没发现新好友,退出助力")
    for i in shareCodes_diff:
        data = postTemplate(cookies, "initForFarm", {
            "shareCode": f"{i}-inviteFriend"})
        helpResult = data["helpResult"]
        print(helpResult)  # 目前code未知
        """-1 为自己   17 已经是好友   0 新增好友   猜测有每日上限"""
        if helpResult["code"] == "0":
            print(f"""成功添加好友 [{helpResult["masterUserInfo"]["nickName"]}]""")
        time.sleep(0.5)

def run():
    for cookies in jdCookie.get_cookies():
        print("######################################")
        print(f"""【 {cookies["pt_pin"]} 】""")
        help(cookies)
        print("\n\n######################################")

if __name__ == "__main__":
    run()
