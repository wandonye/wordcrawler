#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo import APIClient
import webbrowser#python内置的包

APP_KEY = '610318562'
APP_SECRET = 'c721796a9f424d20d232a119a081dac4'
CALLBACK_URL = 'http://still-brook-1028.herokuapp.com'

#利用官方微博SDK
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

access_token = "2.00OyYOXB0mjpSff42868ecb8cOYTKC" # 新浪返回的token，类似abc123xyz456
expires_in = 1563752193
# 设置得到的access_token
client.set_access_token(access_token, expires_in)

#可以打印下看看里面都有什么东西
#print client.friendships.friends.bilateral.ids.get(uid = 1407222942)
pagenum=1
statuses = client.statuses.friends_timeline.get(page=pagenum)['statuses']
length = len(statuses)
print statuses
#输出了部分信息
#for i in range(0,length):
#	print u'昵称：'+statuses[i]['user']['screen_name']
#	print u'简介：'+statuses[i]['user']['description']
#	print u'位置：'+statuses[i]['user']['location']
#	print u'微博：'+statuses[i]['text']