import os, binascii
import sys, getopt

def usage():
	print "usage: python autogen_flask_app.py --githubuser= --githubproject= APP_NAME"

#----------------------------------------
# initialize app constants
#----------------------------------------
optlist, args = getopt.getopt(sys.argv[1:], 'x', ['githubuser=','githubproject=', 'herokuapp='])

if len(args) < 1:
	usage()
	sys.exit()

APP_NAME = args[0]
APP_DIR = APP_NAME

for option, value in optlist:
	if option == '--githubuser':
		GITHUB_USERNAME = value
	if option == '--githubproject':
		GITHUB_REPO_NAME = value
	if option == '--herokuapp':
		HEROKU_APP_NAME = value

#----------------------------------------
# options
#----------------------------------------
DEPLOYMENT = "heroku"
USE_VIRTUALENV_WRAPPER = True

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

FILEDATA_BASE_HTML = """<!DOCTYPE html>
<html lang="en">
  <head>
    {% block head %}
    <title>""" + APP_NAME + """{% block title %}{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="keywords" content="">
    <meta name="author" content="">
    <meta charset="utf-8">

    <meta property="og:title" content=""/>
    <meta property="og:type" content="website"/>
    <meta property="og:url" content=""/>
    <meta property="og:image" content="" />
    <meta property="og:site_name" content='""" + APP_NAME + """'/>
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
              <a class="brand" href="/">""" + APP_NAME + """</a>
              <div class="nav-collapse">
                <ul class="nav">
                </ul>
                {% block navbar_right %}
                <ul class="nav pull-right">
                  {% if not session.logged_in %}
                    <li><a href="#">Login or Signup</a></li>
                  {% else %}
                    <li><a href="#">Logout</a></li>
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
            <p>&copy; """ + APP_NAME + """</p>
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

FILEDATA_404 = """{% extends "base.html" %}
{% block title %} - Page Not Found{% endblock %}
{% block content %}
  <h1>Page Not Found</h1>
  <p><a href="{{ url_for('index') }}">home</a></p>
{% endblock %}"""

#----------------------------------------
# create directory
#----------------------------------------
os.mkdir(APP_DIR)
os.chdir(APP_DIR)

#----------------------------------------
# virtualenv
#----------------------------------------
if USE_VIRTUALENV_WRAPPER:
	os.system('source /usr/local/bin/virtualenvwrapper.sh; mkvirtualenv ' + APP_NAME + '; workon ' + APP_NAME + '; sudo pip install Flask; pip freeze > requirements.txt')
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
if DEPLOYMENT == "heroku":
	try:
		f_procfile = open('Procfile', 'w')
		f_procfile.write('web: python app.py')
		f_procfile.close()
	except IOError:
		pass

#----------------------------------------
# create .gitignore
#----------------------------------------
try:
	f_gitignore = open('.gitignore', 'w')
	f_gitignore.write(FILEDATA_GIT_IGNORE)
	f_gitignore.close()
except IOError:
	pass

#----------------------------------------
# create app.py
#----------------------------------------
try:
	f_apppy = open('app.py', 'w')
	f_apppy.write(FILEDATA_APP_PY)
	f_apppy.close()
except IOError:
	pass

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
try:
	f_basehtml = open('templates/base.html', 'w')
	f_basehtml.write(FILEDATA_BASE_HTML)
	f_basehtml.close()
except IOError:
	pass

try:
	f_indexhtml = open('templates/index.html', 'w')
	f_indexhtml.write(FILEDATA_INDEX_HTML)
	f_indexhtml.close()
except IOError:
	pass

try:
	f_404html = open('templates/404.html', 'w')
	f_404html.write(FILEDATA_404)
	f_404html.close()
except IOError:
	pass

#----------------------------------------
# git commit files
#----------------------------------------
os.system('git add .')
os.system('git commit -m "first commit"')
if GITHUB_USERNAME and GITHUB_REPO_NAME:
	os.system('git remote add origin https://github.com/' + GITHUB_USERNAME + '/' + GITHUB_REPO_NAME + '.git')

#----------------------------------------
# heroku app
#----------------------------------------
if DEPLOYMENT == "heroku" and HEROKU_APP_NAME:
	os.system('heroku git:remote -a ' + HEROKU_APP_NAME)
else:
	os.system('heroku create --stack cedar')
	os.system('heroku apps:rename ' + APP_NAME)

