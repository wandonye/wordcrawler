# -*- coding: utf-8 -*-
"""
	MiniTwit
	~~~~~~~~

	A microblogging application written with Flask and sqlite3.

	:copyright: (c) 2014 by Armin Ronacher.
	:license: BSD, see LICENSE for more details.
"""

import time, codecs, json
import weiboCrawler as wb
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash


# configuration
DATABASE = '/tmp/wangwang.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('WANGWANG_SETTINGS', silent=True)


def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
		top.sqlite_db.row_factory = sqlite3.Row
	return top.sqlite_db


@app.teardown_appcontext
def close_database(exception):
	"""Closes the database again at the end of the request."""
	top = _app_ctx_stack.top
	if hasattr(top, 'sqlite_db'):
		top.sqlite_db.close()


def init_db():
	"""Initializes the database."""
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()


@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	init_db()
	print('Initialized the database.')


def query_db(query, args=(), one=False):
	"""Queries the database and returns a list of dictionaries."""
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	return (rv[0] if rv else None) if one else rv


def get_user_id(username):
	"""Convenience method to look up the id for a username."""
	rv = query_db('select user_id from user where username = ?',
				  [username], one=True)
	return rv[0] if rv else None


def format_datetime(timestamp):
	"""Format a timestamp for display."""
	return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
	"""Return the gravatar image for the given email address."""
	return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
		(md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@app.before_request
def before_request():
	g.user = None
	if 'user_id' in session:
		g.user = query_db('select * from user where user_id = ?',
						  [session['user_id']], one=True)


@app.route('/')
def wordlist():
	"""Shows a users wordlist or if no user is logged in it will
	redirect to login.  
	"""
	if not g.user:
		return redirect(url_for('login'))
	
	# if 'dict' is not in session, if 'wbtoken' is not in session....
	session['dict']='TOEFL'	#for temp test purpose, need to delete and work on choosedict.
		
	dictFile="Dict/"+session['dict']+"dict.dat"
	mydict = json.load(open(dictFile))
	
	words=wb.weiboCrawler(access_token = session['wbtoken'],expires_in = session['wbtokenexpire'], dict=session['dict'], wordnum=session['wordnum'])	
	return render_template('wordlist.html', wordlist={x:mydict[x] for x in words})

#wordlist=query_db('''select user.* from user where user.user_id = ?''',session['user_id'])

#@app.route('/public')
#def public_wordlist():
#	"""Displays the latest messages of all users."""
#	return render_template('wordlist.html', messages=query_db('''
#		select message.*, user.* from message, user
#		where message.author_id = user.user_id
#		order by message.pub_date desc limit ?''', [PER_PAGE]))


#@app.route('/<username>')
#def user_wordlist(username):
#	"""Display's other users wordlist."""
#	profile_user = query_db('select * from user where username = ?',
#							[username], one=True)
#	if profile_user is None:
#		abort(404)
#	followed = False
#	if g.user:
#		words=
#		followed = query_db('''select 1 from follower where
#			follower.who_id = ? and follower.whom_id = ?''',
#			[session['user_id'], profile_user['user_id']],
#			one=True) is not None
#	return render_template('wordlist.html', messages=query_db('''
#			select message.*, user.* from message, user where
#			user.user_id = message.author_id and user.user_id = ?
#			order by message.pub_date desc limit ?''',
#			[profile_user['user_id'], PER_PAGE]), followed=followed,
#			profile_user=profile_user)


#@app.route('/<username>/dict')
#def dict_user(username):
#	"""Adds a dictionary."""
#	if not g.user:
#		abort(401)
#	return redirect(url_for('user_wordlist', username=username))


@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""
	if g.user:
		return redirect(url_for('wordlist'))
	error = None
	if request.method == 'POST':
		user = query_db('''select * from user where
			username = ?''', [request.form['username']], one=True)
		if user is None:
			error = 'Invalid username'
		elif not check_password_hash(user['pw_hash'],
									 request.form['password']):
			error = 'Invalid password'
		else:
			flash('You were logged in')
			session['user_id'] = user['user_id']
			if user['wbtoken'] is None:
				return redirect(url_for('linkwb'))
			session['wbtoken'] = user['wbtoken']
			session['wbtokenexpire'] = user['wbtokenexpire']
			if user['dict'] is None:
				return redirect(url_for('choosedict'))
			session['dict']= user['dict']
			session['wordnum']=100
			return redirect(url_for('wordlist'))
	return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Registers the user."""
	if g.user:
		return redirect(url_for('wordlist'))
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['email'] or \
				'@' not in request.form['email']:
			error = 'You have to enter a valid email address'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif get_user_id(request.form['username']) is not None:
			error = 'The username is already taken'
		else:
			db = get_db()
			db.execute('''insert into user (
			  username, email, pw_hash) values (?, ?, ?)''',
			  [request.form['username'], request.form['email'],
			   generate_password_hash(request.form['password'])])
			db.commit()
			flash('You were successfully registered and can login now')
			return redirect(url_for('login'))
	return render_template('register.html', error=error)


@app.route('/logout')
def logout():
	"""Logs the user out."""
	flash('You were logged out')
	session.pop('user_id', None)
	return redirect(url_for('login'))

@app.route('/choosedict')
def choosedict():
	"""choose dict."""
	return render_template('choosedict.html', dicts)
	
@app.route('/linkwb')
def linkwb():

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
		return render_template('linkwb.html',url=url)
		
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
			return render_template('linkwb.html',url=url)
		
		#write token to db	
		db = get_db()
		db.execute('''update user set wbtoken = ?, wbtokenexpire=? WHERE user_id = ?''',
					[r.access_token,r.expires_in,session['user_id']])
		db.commit()
		
		#write token to session
		session['wbtoken']=r.access_token
		session['wbtokenexpire'] = r.expires_in
		
		if 'dict' in session:
			return redirect(url_for('wordlist'))
		else:
			redirect(url_for('choosedict'))

# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url
