import os, binascii
import sys, getopt

#----------------------------------------
# settings
#----------------------------------------

virtualenvwrapper_path = '/usr/local/bin/virtualenvwrapper.sh'
hosts_path = '/etc/hosts'

#----------------------------------------
# usage and help functions
#----------------------------------------
def usage(method=None, addon=None):
	usage_base = "usage: python generator.py "
	usage_create = "--githubuser= create APP_NAME"
	usage_options = "options: 'githubuser=', 'githubproject=', 'herokuapp=', 'novirtualenvwrapper', 'useexistingherokuapp'"
	usage_addon_fblogin = "addon <app_dir> fblogin <fb_appid> <fb_appsecret> <deployment_url>"
	userage_addon_mongodb_for_fblogin = "addon <app_dir> mongodb_for_fblogin <db_name> <db_user> <db_pw> <db_hostaddr>"
	print ""
	if method == 'addon':
		print usage_base + usage_addon_fblogin + "\n"
		print usage_base + userage_addon_mongodb_for_fblogin + "\n"
	else:
		print usage_base + usage_create + "\n" + usage_options + "\n"
		print usage_base + usage_addon_fblogin + "\n"
		print usage_base + userage_addon_mongodb_for_fblogin + "\n"

#----------------------------------------
# initialize file data
#----------------------------------------
FILEDATA_GIT_IGNORE = """*.pyc
venv
*~
.DS_Store
ignore"""

FILEDATA_APP_PY = """import os
from flask import Flask, render_template, send_from_directory

#----------------------------------------
# initialization
#----------------------------------------

app = Flask(__name__)

app.config.update(
	DEBUG = True,
)

app.config["SECRET_KEY"] = '""" + binascii.b2a_hex(os.urandom(24)) + """'

### marker for flask app generator - keep this line

#----------------------------------------
# controllers
#----------------------------------------

@app.route("/")
def index():
	return render_template('index.html')

#----------------------------------------
# handlers
#----------------------------------------

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)"""

def render_models_code():
	return """import datetime

class User(db.DynamicDocument):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

	facebook_id = db.IntField(required=True, unique=True)
	name = db.StringField(max_length=255, required=True)

	def __unicode__(self):
		return self.name

	meta = {
		'indexes' : ['-created_at', 'facebook_id'],
		'ordering' : ['-created_at']
	}"""

def render_mongoengine_code(db_name, db_username, db_password, db_host_address):
	return """#----------------------------------------
# database
#----------------------------------------

from mongoengine import connect
from flask.ext.mongoengine import MongoEngine
from models import *

DB_NAME = '""" + db_name + """'
DB_USERNAME = '""" + db_username + """'
DB_PASSWORD = '""" + db_password + """'
DB_HOST_ADDRESS = '""" + db_host_address + """'

app.config["MONGODB_DB"] = DB_NAME
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
db = MongoEngine(app)

def get_user_from_db(facebook_id):
	if not facebook_id:
		raise ValueError()
	users_found = User.objects(facebook_id=facebook_id)
	if len(users_found) == 1:
		return users_found[0]
	elif len(users_found) == 0:
		return None
	else:
		raise Exception('Database Integrity Error')

def save_user_to_db(facebook_id, name):
	user = User()
	user.facebook_id = facebook_id
	user.name = name
	try:
		user.save()
	except:
		raise Exception('Could not save user to database.')
"""

def render_fb_authentication_code(fb_appid, fb_appsecret, scope='email, '):
	return """#----------------------------------------
# facebook authentication
#----------------------------------------

from flask import url_for, request, session, redirect
from flask_oauth import OAuth

FACEBOOK_APP_ID = '""" + fb_appid + """'
FACEBOOK_APP_SECRET = '""" + fb_appsecret + """'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
	base_url='https://graph.facebook.com/',
	request_token_url=None,
	access_token_url='/oauth/access_token',
	authorize_url='https://www.facebook.com/dialog/oauth',
	consumer_key=FACEBOOK_APP_ID,
	consumer_secret=FACEBOOK_APP_SECRET,
	request_token_params={'scope': ('""" + scope + """')}
)

@facebook.tokengetter
def get_facebook_token():
	return session.get('facebook_token')

def pop_login_session():
	session.pop('logged_in', None)
	session.pop('facebook_token', None)

@app.route("/facebook_login")
def facebook_login():
	return facebook.authorize(callback=url_for('facebook_authorized',
		next=request.args.get('next'), _external=True))

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
	next_url = request.args.get('next') or url_for('index')
	if resp is None or 'access_token' not in resp:
		return redirect(next_url)

	session['logged_in'] = True
	session['facebook_token'] = (resp['access_token'], '')

	data = facebook.get('/me').data
	if 'id' in data and 'name' in data:
		facebook_id = data['id']
		name = data['name']

	### if user is new, save user data to database

	return redirect(next_url)

@app.route("/logout")
def logout():
	pop_login_session()
	return redirect(url_for('index'))"""

def render_base_html(app_name):
	return """<!DOCTYPE html>
<html lang="en">
  <head>
	{% block head %}
	<title>""" + app_name + """{% block title %}{% endblock %}</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="">
	<meta name="keywords" content="">
	<meta name="author" content="">
	<meta charset="utf-8">

	<meta property="og:title" content=""/>
	<meta property="og:type" content="website"/>
	<meta property="og:url" content=""/>
	<meta property="og:image" content="" />
	<meta property="og:site_name" content='""" + app_name + """'/>
	<meta property="og:description" content=""/>

	<link href="http://twitter.github.com/bootstrap/assets/css/bootstrap.css" rel="stylesheet">
	<style> body { padding-top: 60px; } </style>

	<!-- SUPPORT FOR IE6-8 OF HTML5 ELEMENTS -->
	<!--[if lt IE 9]>
		  <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
	<![endif]-->

	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>

	<script src="http://twitter.github.com/bootstrap/assets/js/bootstrap.js"></script>
	{% endblock %}
  </head>

  <body>

	{% block navbar %}
	<div class="navbar navbar-fixed-top">
		<div class="navbar-inner">
			<div class="container">
			  <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
			  </a>
			  <a class="brand" href="/">""" + app_name + """</a>
			  <div class="nav-collapse">
				<ul class="nav">
				</ul>
				{% block navbar_right %}
				<ul class="nav pull-right">
				  {% if not session.logged_in %}
					<li><a id="navbar_login_button" href="#">Login or Signup</a></li>
				  {% else %}
					<li><a id="navbar_logout_button" href="#">Logout</a></li>
				  {% endif %}
				</ul>
				{% endblock %}
			  </div><!--/.nav-collapse -->
			</div>
		  </div>
	</div>
	{% endblock %}

	<div class="container page">
		<div class="content">
		  {% block content %}
		  {% endblock %}
		</div>

		<hr>

		{% block footer %}
		<footer class="footer">
			<p>&copy; """ + app_name + """</p>
		</footer>
		{% endblock %}
	</div>
  </body>
</html>"""

FILEDATA_INDEX_HTML = """{% extends "base.html" %}
{% block content %}
{% if not session.logged_in %}
	 <p>You are not logged in.</p>
{% else %}
	 <p>You are logged in.</p>
{% endif %}
{% endblock %}"""

FILEDATA_404_HTML = """{% extends "base.html" %}
{% block title %} - Page Not Found{% endblock %}
{% block content %}
  <h1>Page Not Found</h1>
  <p><a href="{{ url_for('index') }}">home</a></p>
{% endblock %}"""

#----------------------------------------
# CREATE APP
#----------------------------------------
def create_app(app_name, filedata,
	app_dir=None,
	hosting_platform="heroku",
	use_virtualenv_wrapper=False,
	github_username=None,
	github_project=None,
	heroku_app_name=None,
	use_existing_heroku_project=False):

	if app_dir is None:
		app_dir = app_name

	#----------------------------------------
	# create directory
	#----------------------------------------
	os.mkdir(app_dir)
	os.chdir(app_dir)

	#----------------------------------------
	# virtualenv
	#----------------------------------------
	if use_virtualenv_wrapper:
		os.system('source ' + virtualenvwrapper_path + '; mkvirtualenv ' + app_name + '; workon ' + app_name + '; sudo pip install Flask; pip freeze > requirements.txt')
	else:
		os.system('virtualenv venv --distribute')
		os.system('source venv/bin/activate; sudo pip install Flask; pip freeze > requirements.txt')

	#----------------------------------------
	# initialize Git
	#----------------------------------------
	os.system('git init')

	#----------------------------------------
	# create README
	#----------------------------------------
	os.system('touch README.md')

	#----------------------------------------
	# create Procfile
	#----------------------------------------
	if hosting_platform == "heroku":
		with open('Procfile', 'w') as f:
			f.write('web: python app.py')

	#----------------------------------------
	# create .gitignore
	#----------------------------------------
	if 'gitignore' in filedata:
		with open('.gitignore', 'w') as f:
			f.write(filedata['gitignore'])

	#----------------------------------------
	# create app.py
	#----------------------------------------
	if 'mainapp' in filedata:
		with open('app.py', 'w') as f:
			f.write(filedata['mainapp'])

	#----------------------------------------
	# directories for templates and statics
	#----------------------------------------
	os.mkdir('templates')
	os.mkdir('static')
	os.makedirs('static/css')
	os.makedirs('static/js')
	os.makedirs('static/img')
	os.makedirs('static/ico')

	#----------------------------------------
	# create basic templates
	#----------------------------------------
	if 'basetemplate' in filedata:
		with open('templates/base.html', 'w') as f:
			f.write(filedata['basetemplate'])
	if 'indextemplate' in filedata:
		with open('templates/index.html', 'w') as f:
			f.write(filedata['indextemplate'])
	if '404template' in filedata:
		with open('templates/404.html', 'w') as f:
			f.write(filedata['404template'])

	#----------------------------------------
	# git commit files
	#----------------------------------------
	os.system('git add .')
	os.system('git commit -m "first commit"')
	if github_username and github_project:
		os.system('git remote add origin https://github.com/' + github_username + '/' + github_project + '.git')

	#----------------------------------------
	# heroku app
	#----------------------------------------
	if hosting_platform == "heroku" and heroku_app_name:
		if use_existing_heroku_project:
			os.system('heroku git:remote -a ' + heroku_app_name)
		else:
			os.system('heroku create --stack cedar')
			os.system('heroku apps:rename ' + heroku_app_name)

def add_to_app(app_dir, virtualenv_name, addon, data={}):
	os.chdir(app_dir)

	if addon == 'fblogin':
		if 'fb_appid' in data and 'fb_appsecret' in data and 'deployment_url' in data:
			os.system('source ' + virtualenvwrapper_path + '; workon ' + virtualenv_name + '; sudo pip install Flask-OAuth; pip freeze > requirements.txt')

			fb_authentication_code = render_fb_authentication_code(data['fb_appid'], data['fb_appsecret'])

			with open("app.py", 'r') as f:
				filedata = f.read()
			filedata = filedata.replace('### marker for flask app generator - keep this line', '### marker for flask app generator - keep this line\n\n' + fb_authentication_code)
			with open("app.py", 'w') as f:
				f.write(filedata)

			deployment_url = data['deployment_url'].strip('http://').strip('https://').strip('/')

			with open(hosts_path, "a") as f:
				f.write("\n127.0.0.1 a." + deployment_url)

			with open("templates/base.html", 'r') as f:
				filedata = f.read()
			filedata = filedata.replace('id="navbar_login_button" href="#"', 'id="navbar_login_button" href="/facebook_login"')
			filedata = filedata.replace('id="navbar_logout_button" href="#"', 'id="navbar_logout_button" href="/logout"')
			with open("templates/base.html", 'w') as f:
				f.write(filedata)

			print 'fblogin installed! start up your app and visit http://a.' + deployment_url + ':5000 to see it in action'
		else:
			usage(method='addon', addon='fblogin')
			sys.exit()
	elif addon == 'mongodb_for_fblogin':
		if 'db_name' in data and 'db_user' in data and 'db_password' in data and 'db_host_address' in data:
			os.system('source ' + virtualenvwrapper_path + '; workon ' + virtualenv_name + '; sudo pip install mongoengine flask_mongoengine; pip freeze > requirements.txt')

			mongoengine_code = render_mongoengine_code(data['db_name'], data['db_user'], data['db_password'], data['db_host_address'])

			with open("app.py", 'r') as f:
				filedata = f.read()
			filedata = filedata.replace('### marker for flask app generator - keep this line', mongoengine_code + '\n### marker for flask app generator - keep this line')
			filedata = filedata.replace('### if user is new, save user data to database', 'user = get_user_from_db(facebook_id)\n\tif user is None:\n\t\tsave_user_to_db(facebook_id, name)')
			with open("app.py", 'w') as f:
				f.write(filedata)

			models_code = render_models_code()

			with open("models.py", 'w') as f:
				f.write(models_code)
		else:
			usage(method='addon', addon='mongodb_for_fblogin')
			sys.exit()
	else:
		usage(method='addon')
		sys.exit()

#----------------------------------------
# PARSE OPTS AND ARGS AND CALL METHOD
#----------------------------------------
optlist, args = getopt.getopt(sys.argv[1:], '', ['githubuser=', 'githubproject=', 'herokuapp=', 'novirtualenvwrapper', 'useexistingherokuapp'])

if len(args) < 1:
	usage()
	sys.exit()
method = args[0]

if method == 'create':
	if len(args) < 2:
		usage()
		sys.exit()
	app_name = args[1]

	github_username = None
	github_project = app_name
	heroku_app_name = app_name
	app_dir = app_name
	use_virtualenv_wrapper = True
	use_existing_heroku_project = False
	for option, value in optlist:
		if option == '--githubuser':
			github_username = value
		if option == '--githubproject':
			github_project = value
		if option == '--herokuapp':
			heroku_app_name = value
		if option == '--novirtualenvwrapper':
			use_virtualenv_wrapper = False
		if option == '--useexistingherokuapp':
			use_existing_heroku_project = True

	filedata = {
		'gitignore': FILEDATA_GIT_IGNORE,
		'mainapp': FILEDATA_APP_PY,
		'basetemplate': render_base_html(app_name),
		'indextemplate': FILEDATA_INDEX_HTML,
		'404template': FILEDATA_404_HTML,
	}

	create_app(app_name, filedata,
		app_dir=app_dir,
		use_virtualenv_wrapper=use_virtualenv_wrapper,
		github_username=github_username,
		github_project=github_project,
		heroku_app_name=heroku_app_name,
		use_existing_heroku_project=use_existing_heroku_project)
elif method == 'addon':
	if len(args) < 3:
		usage()
		sys.exit()
	app_dir = args[1]
	virtualenv_name = app_dir
	addon = args[2]

	if addon == 'fblogin':
		if len(args) < 6:
			usage()
			sys.exit()
		fb_appid = args[3]
		fb_appsecret = args[4]
		deployment_url = args[5]

		add_to_app(app_dir, virtualenv_name, addon, data={'fb_appid': fb_appid, 'fb_appsecret': fb_appsecret, 'deployment_url': deployment_url })
	elif addon == 'mongodb_for_fblogin':
		if len(args) < 7:
			usage()
			sys.exit()
		db_name = args[3]
		db_user = args[4]
		db_password = args[5]
		db_host_address = args[6]

		add_to_app(app_dir, virtualenv_name, addon, data={'db_name': db_name, 'db_user': db_user, 'db_password': db_password, 'db_host_address': db_host_address })
	else:
		usage()
		sys.exit()
else:
	usage()
	sys.exit()

