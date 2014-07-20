# _*_ coding: utf-8 _*_
from weibo import APIClient
import webbrowser

from flask import Flask,render_template
app = Flask(__name__)


#webbrowser.open_new(url)
# 获取URL参数code:
#code = '2fc0b2f5d2985db832fa01fee6bd9316'
#client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
#r = client.request_access_token(code)
#access_token = r.access_token # 新浪返回的token，类似abc123xyz456
#expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
# TODO: 在此可保存access token
#print access_token, expires_in
#client.set_access_token(access_token, expires_in)

#print client.friendships.friends.bilateral.ids.get(uid = 12345678)

@app.route('/')
def home():

	APP_KEY = '610318562'
	APP_SECRET = 'c721796a9f424d20d232a119a081dac4'
	CALLBACK_URL = 'http://still-brook-1028.herokuapp.com'
	#这个是设置回调地址，必须与那个”高级信息“里的一致
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	url = client.get_authorize_url()
	# TODO: redirect to url
	return render_template('home.html',url=url)
	code = '4963afb83e6fa5fad0d40e73753babf0'
	r = client.request_access_token(code)
	expires_in = r.expires_in
	print access_token, expires_in
	client.set_access_token(access_token, expires_in)
	print client.friendships.friends.bilateral.ids.get(uid = 12345678)
    
if __name__ == '__main__':
    app.run()
    #app.run(host='0.0.0.0')