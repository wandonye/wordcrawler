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

	APP_KEY = '162581389'
	APP_SECRET = '91f1a7d9f52df405f0273b55c2edaa0f'
	CALLBACK_URL = 'http://condorism.com'
	#这个是设置回调地址，必须与那个”高级信息“里的一致
	client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
	url = client.get_authorize_url()
	# TODO: redirect to url
#	print url
	return render_template('home.html',url=url)
    
if __name__ == '__main__':
    app.run()
    #app.run(host='0.0.0.0')