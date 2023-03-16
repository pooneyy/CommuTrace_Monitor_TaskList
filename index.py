#!/usr/bin/env python3
# -*- coding: utf8 -*-
'''
Author       : Qiuyelin
Date         : 2023-03-14 20:08:52
LastEditors  : Qiuyelin 85266337+pooneyy@users.noreply.github.com
LastEditTime : 2023-03-16 17:14:58
FilePath     : /CommuTrace_Monitor_TaskList/index.py
Description  : 共迹算力平台_监听任务列表

Copyright (c) 2023 by 秋夜临, All Rights Reserved. 
'''

import base64
import json
import os
import re
import datetime, pytz, time
import sys
import requests

VERSION = 0.1
CONFIG_VERSION = 0.1
HOST = "http://39.101.72.182/index.php/"

def timeStamp_To_dateTime(timeStamp):
    return datetime.datetime.fromtimestamp(int(timeStamp), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

def saveConfig(config):
    with open("config.json", "w", encoding='utf8') as file:
        json.dump(config, file, ensure_ascii=False, indent = 4)

def init():
    print('首次运行初始化')
    config = {}
    config['config_version'] = CONFIG_VERSION
    config['latestOrderID'] = 0
    config['commutrace_username'] = input('请输入平台算力用户账号：')
    config['commutrace_password'] = input('请输入密码：')
    config['truecaptcha_userid'] = input('请输入truecaptcha的userid：')
    config['truecaptcha_apikey'] = input('请输入truecaptcha的apikey：')
    config['pushplus_token'] = input('请输入pushplus推送加的token：')
    config['pushplus_topic'] = input('(选填)输入pushplus推送加的群组编码：')
    saveConfig(config)
    print('初始化完成，请重新运行')

def loadConfig():
    with open("config.json", "r+", encoding='utf8') as file:
        config = json.load(file)
    return config

def sendMsg(config, msg):
    data = {}
    url = "http://www.pushplus.plus/send"
    data['token'] = config['pushplus_token']
    data['title'] = 'CommuTrace 共迹算力共享平台'
    data['template'] = 'markdown'
    data['topic'] = config['pushplus_topic'] # 群组编码，发送群组消息。
    data['content'] = msg
    response = requests.post(url,data=data)
    return response.text

def apitruecaptcha(config, content):
    image=base64.b64encode(content)
    url = 'https://api.apitruecaptcha.org/one/gettext'
    data = {
        'data':str(image,'utf-8'),
        'userid':config['truecaptcha_userid'],
        'apikey':config['truecaptcha_apikey']
    }
    result = requests.post(url, json.dumps(data))
    res=result.json()
    try:verifycode = res['result']
    except:
        print("TrueCaptcha已达每日请求上限，无法再识别验证码。")
        os._exit(0)
    return verifycode

def getCookie():
    url = f"{HOST}/Home/Login/login.html"
    response = requests.get(url)
    return response.cookies

def getCaptchaImage(cookies):
    url = f"{HOST}/Home/Login/verify.html"
    response = requests.get(url, cookies=cookies)
    image = response.content
    return image

def login(config):
    cookies = getCookie()
    captchaImage = getCaptchaImage(cookies)
    verifycode = apitruecaptcha(config, captchaImage)
    url = f"{HOST}/Home/Login/dologin.html"
    payload={
        'type': 2,
        'username': config['commutrace_username'],
        'password': config['commutrace_password'],
        'verifycode': verifycode
    }
    response = requests.post(url, cookies=cookies, data=payload)
    print(f"{timeStamp_To_dateTime(time.time())}\t登录成功")
    return cookies

def getAllorder(cookies):
    '''获取全部订单'''
    url = f"{HOST}/Home/Index/allorder.html"
    response = requests.get(url, cookies=cookies)
    return response.text

def analyzingAllorder(allorder):
    '''分析订单页面'''
    if '请在登录后操作' in allorder:return 0
    else:
        taskData = re.findall(r'<td>[\s\S]+<\/td>', allorder)[0]
        createTime = re.findall(r"(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)", taskData)[0][0]
        taskData = re.sub(r"(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)", f"{createTime}_" ,taskData)
        taskData = taskData.replace("\"" , "\'")
        taskData = taskData.replace(' ' , '')
        taskData = taskData.replace('\t' , '')
        taskData = taskData.replace('\r\n' , '')
        # if 'tr' in taskData: taskData = re.sub(r"(<.?tr>)", r"" ,taskData)
        taskData = re.sub(r"(<.?tr>)", r"" ,taskData)
        taskData = taskData.replace('</td><td>' , '</td>,<td>')
        taskData = re.sub(r"(<.?td>)", r'"' ,taskData)
        taskData = json.loads("[" + taskData + "]")
        n = 8 # 分割列表，每8项为一组
        taskValue = []
        taskKeys = ['orderID', 'orderName', 'orderDetail', 'createTime', 'unitIncome', 'completed_and_Total', 'number_of_Participants', 'applyOrder']
        taskList = []
        for i in range(0, len(taskData), n):
            taskValue = taskData[i:i + n]
            taskDict = dict(zip(taskKeys, taskValue))
            taskList.append(taskDict)
        return taskList

def taskList_To_Msg(taskList):
    msg = f'''
| 订单号 | 订单细节 | 创建时间 | 单位收益 | 完成量/总量 |
| :----: | :------: | :------: | :------: | :------: |
'''
    for i in taskList:
        msg += f"|{i['orderID']}|{i['orderDetail']}|{i['createTime']}|{i['unitIncome']}|{i['completed_and_Total']}|"
    msg += timeStamp_To_dateTime(time.time())
    return msg

def loop(config):
    cookies = login(config)
    while True:
        taskList = analyzingAllorder(getAllorder(cookies))
        if taskList == 0 :
            cookies = login(cookies)
            continue
        i = [i['orderID'] for i in taskList] # 列表，临时存储订单ID用于寻找最大的ID
        latestOrderID = int(max(i))
        if latestOrderID > config['latestOrderID']:
            config['latestOrderID'] = latestOrderID
            msg = f"#### 有新订单。当前最新是 {latestOrderID}\n"
            msg += taskList_To_Msg(taskList)
            sendMsg(config, msg)
            saveConfig(config)
            print(f"{taskList_To_Msg(taskList)}\n")
        print(f"刷新于 {timeStamp_To_dateTime(time.time())}\r",end='')
        time.sleep(30)
    ...

def main():
    if 'linux' in sys.platform: sys.stdout.write(f"\x1b]2;监听共迹任务列表 - 版本 {VERSION}\x07")
    elif 'win' in sys.platform: os.system(f"title 监听共迹任务列表 - 版本 {VERSION}")
    try:
        config = loadConfig()
        try:loop(config)
        except KeyboardInterrupt:print("结束")
    except FileNotFoundError:init()
    ...

if __name__ == '__main__':
    main()
    ...