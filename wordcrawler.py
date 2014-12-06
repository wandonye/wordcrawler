# _*_ coding: utf-8 _*_
from weibo import APIClient
import os.path, time

from flask import Flask,request,render_template,url_for
app = Flask(__name__)


@app.route('/')
def home():

	code = request.args.get('code')

	if code is None:	
		APP_KEY = '610318562'
		APP_SECRET = 'c721796a9f424d20d232a119a081dac4'
		CALLBACK_URL = 'http://still-brook-1028.herokuapp.com'
		#这个是设置回调地址，必须与那个”高级信息“里的一致
		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		url = client.get_authorize_url()
		# TODO: redirect to url
		#print access_token, expires_in
		#print client.friendships.friends.bilateral.ids.get(uid = 12345678)
		return render_template('home.html',url=url)
		
	else:
		APP_KEY = '610318562'
		APP_SECRET = 'c721796a9f424d20d232a119a081dac4'
		CALLBACK_URL = 'http://still-brook-1028.herokuapp.com'
		#这个是设置回调地址，必须与那个”高级信息“里的一致
		client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
		try:
			r = client.request_access_token(code)
		except:			#if code is invalid
			url = client.get_authorize_url()
			return render_template('home.html',url=url)
		access_token=r.access_token
		expires_in = r.expires_in
		client.set_access_token(access_token, expires_in)
		
		pagenum=1
		content=client.statuses.friends_timeline.get(page=pagenum)['statuses']
		#content= client.statuses.home_timeline.get(uid = 1407222942)
		#uid = 1407222942
		length=len(content)
		wbtext=''
		for i in range(0,length):
			wbtext+=content[i]['text']
			wbtext+='\n'

		return render_template('content.html',token=access_token,exp=expires_in,content=wbtext)

		
    
if __name__ == '__main__':
    app.run(debug=True)
    
    #app.run(host='0.0.0.0')