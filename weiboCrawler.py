#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo import APIClient
import webbrowser, datetime, time, goslate, pytz, json, azure_translate_api
from dateutil import parser
#import bingtranslate as bing

def weiboCrawler(access_token = "2.00OyYOXB0mjpSff42868ecb8cOYTKC",expires_in = 1563752193, dict='TOEFL', wordnum=100):
	APP_KEY = '610318562'
	APP_SECRET = 'c721796a9f424d20d232a119a081dac4'
	CALLBACK_URL = 'http://still-brook-1028.herokuapp.com'

	#利用官方微博SDK
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

	# 设置得到的access_token
	client.set_access_token(access_token, expires_in)

	#可以打印下看看里面都有什么东西
	#print client.friendships.friends.bilateral.ids.get(uid = 1407222942)

	fileName='Dict/'+dict+'ASC.txt'
	Twords = set(line.strip() for line in open(fileName))

	words=[]
	pagenum=1
	hasmore=True
	wbbitext=wbgotext=entext=''
	#loc_zone = pytz.timezone('US/Eastern')
	loc_zone = pytz.timezone('Asia/Seoul')
	bj_zone=pytz.timezone('Asia/Shanghai')
	while hasmore:
		statuses = client.statuses.friends_timeline.get(page=pagenum)['statuses']
		length = len(statuses)
		#print statuses
		#输出了部分信息
		for i in range(0,length):
		#	print u'昵称：'+statuses[i]['user']['screen_name']
		#	print u'时间：'+statuses[i]['created_at']
#			print u'微博：'+statuses[i]['text']
			wbbitext+=statuses[i]['text']
		#	wbgotext+=statuses[i]['text']
			if len(wbbitext)>1800:			#bing translate has length limit
				wbbitext=wbbitext.encode('utf-8')
				bingclient = azure_translate_api.MicrosoftTranslatorClient('wangwangxianbei_2014',  # make sure to replace client_id with your client id
																	   'ZhzP5sHEpYemPvnccRxO5dfc6Oytxi2ZrfZfDwTQG60=') # replace the client secret with the client secret for you app.
				entext=bingclient.TranslateText(wbbitext, 'zh-CHS', 'en')				
				newwords=entext.split(' ')
				realwords={x for x in newwords if x in Twords}
			
				words.extend(realwords)
				words=list(set(words))
				wbbitext=''
				if len(words)>wordnum:
					hasmore=False
					break

			wbtime= parser.parse(statuses[i]['created_at'])
			now = datetime.datetime.now()
			lasttime=loc_zone.localize(now.replace(hour=0, minute=0, second=0, microsecond=0))
			bjlasttime=lasttime.astimezone(bj_zone)
			if wbtime<lasttime:
				hasmore=False
		pagenum+=1

	########google translate engine, free but slow################
	#gs = goslate.Goslate()
	#entext= gs.translate(wbgotext, 'en')


	#http://fanyi.youdao.com/openapi.do?keyfrom=<keyfrom>&key=<key>&type=data&doctype=jsonp&callback=show&version=1.1&q=API


	return realwords

if __name__ == '__main__':

	print weiboCrawler()
			
