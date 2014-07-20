# _*_ coding: utf-8 _*_
from weibo import APIClient
import webbrowser

from flask import Flask,render_template
app = Flask(__name__)


#webbrowser.open_new(url)
@app.route('/?code=<code>')
def show_data(code):
    # show the user profile for that user
#	code = '4963afb83e6fa5fad0d40e73753babf0'
	r = client.request_access_token(code)
	expires_in = r.expires_in
#	print access_token, expires_in
	client.set_access_token(access_token, expires_in)
	content= client.friendships.friends.bilateral.ids.get(uid = 12345678)

	return render_template('content.html',token=access_token,exp=expires_in,content=content)

#	return 'User %s' % username

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
    
if __name__ == '__main__':
    app.run()
    #app.run(host='0.0.0.0')