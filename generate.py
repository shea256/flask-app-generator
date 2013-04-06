import os
import binascii
import argparse

favicon_url = 'http://twitter.github.io/bootstrap/assets/ico/favicon.png'
jquery_url = 'http://code.jquery.com/jquery-1.8.3.js'
jquerymin_url = 'http://code.jquery.com/jquery-1.8.3.min.js'
bootstrapjs_url = 'http://twitter.github.io/bootstrap/assets/js/bootstrap.js'
bootstrapjsmin_url = 'http://twitter.github.io/bootstrap/assets/js/bootstrap.min.js'
bootstrapcss_url = 'http://twitter.github.io/bootstrap/assets/css/bootstrap.css'

def git_add_and_commit(message):
	os.system('git add .')
	os.system('git commit -m "' + message + '"')

def create_app_files(app_name):
	#----------------------------------------
	# create directory
	#----------------------------------------
	os.mkdir(app_name)
	os.chdir(app_name)

	#----------------------------------------
	# git files
	#----------------------------------------
	os.system('git init')
	os.system('touch README.md')

	with open('.gitignore', 'w') as f:
		f.write(render_filedata('gitignore'))

	#----------------------------------------
	# heroku files
	#----------------------------------------
	with open('Procfile', 'w') as f:
		f.write(render_filedata('procfile'))

	#----------------------------------------
	# python files
	#----------------------------------------
	with open('app.py', 'w') as f:
		f.write(render_filedata('main_app'))

	#----------------------------------------
	# templates
	#----------------------------------------
	os.mkdir('templates')

	with open('templates/base.html', 'w') as f:
		f.write(render_filedata('base_template', app_name=app_name))

	with open('templates/index.html', 'w') as f:
		f.write(render_filedata('index_template', app_name=app_name))

	with open('templates/404.html', 'w') as f:
		f.write(render_filedata('404_template'))

	#----------------------------------------
	# static files
	#----------------------------------------
	os.mkdir('static')
	os.makedirs('static/css')
	os.makedirs('static/js')
	os.makedirs('static/img')
	os.makedirs('static/ico')

	os.system('curl ' + bootstrapcss_url + ' > static/css/bootstrap.css')
	os.system('curl ' + bootstrapjs_url + ' > static/js/bootstrap.js')
	os.system('curl ' + bootstrapjsmin_url + ' > static/js/bootstrap.min.js')
	os.system('curl ' + jquery_url + ' > static/js/jquery.js')
	os.system('curl ' + jquerymin_url + ' > static/js/jquery.min.js')
	os.system('curl ' + favicon_url + ' > static/ico/favicon.ico')

def configure_github(github_user, github_repo):
	os.system('git remote add origin https://github.com/' + github_user + '/' + github_repo + '.git')

def configure_heroku(heroku_app):
	os.system('heroku create --stack cedar')
	os.system('heroku apps:rename ' + heroku_app)

def configure_virtualenvwrapper(app_name, virtualenvwrapper_path):
	os.system('source ' + virtualenvwrapper_path + '; mkvirtualenv ' + app_name + '; workon ' + app_name + '; sudo pip install Flask; pip freeze > requirements.txt')

def configure_virtualenv(app_name):
	os.system('virtualenv venv --distribute; source venv/bin/activate; sudo pip install Flask; pip freeze > requirements.txt')

def main():
	#----------------------------------------
	# parse arguments
	#----------------------------------------
	parser = argparse.ArgumentParser(description='Autogenerate a Flask app')
	parser.add_argument('appname', help='the name of the app to be created')
	parser.add_argument('--githubuser', dest='github_user', help='the name of the github user that will be hosting the app')
	parser.add_argument('--githubrepo', dest='github_repo', help='the name of the remote github repo that will be hosting the app')
	parser.add_argument('--herokuapp', dest='heroku_app', help='the name that the heroku app will be renamed to if it has not yet been taken')
	parser.add_argument('--venvname', dest='virtualenv_name', help='the name of the virtualenv for the app')
	parser.add_argument('--venvwrapperpath', dest='virtualenvwrapper_path', help='the path to the file virtualenvwrapper.sh (turns on virtualenvwrapper when specified)')
	parser.add_argument('--push', dest='push', help='automatically push to github and heroku when app has been created', action='store_true')
	args = parser.parse_args()

	#----------------------------------------
	# create app files
	#----------------------------------------
	create_app_files(args.appname)

	#----------------------------------------
	# configure github
	#----------------------------------------
	if args.github_user and args.github_repo:
		configure_github(args.github_user, args.github_repo)

	#----------------------------------------
	# configure heroku
	#----------------------------------------
	if args.heroku_app:
		configure_heroku(args.heroku_app)

	#----------------------------------------
	# configure virtualenv
	#----------------------------------------
	if args.virtualenv_name:
		if args.virtualenvwrapper_path:
			configure_virtualenvwrapper(args.virtualenv_name, args.virtualenvwrapper_path)
		else:
			configure_virtualenv(args.virtualenv_name)

	#----------------------------------------
	# commit all files
	#----------------------------------------
	git_add_and_commit('first commit')

	#----------------------------------------
	# push to github and heroku
	#----------------------------------------
	if args.push:
		if args.github_user and args.github_repo:
			os.system('git push origin master')
		if args.heroku_app:
			os.system('git push heroku master; heroku open')

	#----------------------------------------
	# print success message
	#----------------------------------------
	print "\nYour app has been created!"

def render_filedata(filename, **kwargs):
	if filename == 'gitignore':
		return """*.pyc\nvenv\n*~\n.DS_Store\nignore"""
	elif filename == 'procfile':
		return """web: python app.py"""
	elif filename == 'main_app':
		return """import os
from flask import Flask, render_template, send_from_directory, Response, url_for, request
import json

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
	elif filename == 'base_template':
		if 'app_name' not in kwargs:
			raise Exception('Rendering base_template requires the "app_name" keyword argument.')
		else:
			app_name = kwargs['app_name']
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

	<link href="{{ url_for('static', filename='css/bootstrap.css') }}" rel="stylesheet">
	<style> body { padding-top: 60px; } </style>

	<!-- SUPPORT FOR IE6-8 OF HTML5 ELEMENTS -->
	<!--[if lt IE 9]>
		  <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
	<![endif]-->

	<script src="{{ url_for('static', filename='js/jquery.min.js') }}"></script>
	<script src="{{ url_for('static', filename='js/bootstrap.min.js') }}"></script>
	{% endblock %}
  </head>

  <body>

	{% block navbar %}
	<div class="navbar navbar-fixed-top">
		<div class="navbar-inner">
			<div class="container">
			  <a class="brand" href="/">""" + app_name + """</a>
			  <div class="nav-collapse">
				<ul class="nav">
				</ul>
				{% block navbar_right %}
				<ul class="nav pull-right">
					<li><a href="/">Home</a></li>
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
	elif filename == 'index_template':
		if 'app_name' not in kwargs:
			raise Exception('Rendering index_template requires the "app_name" keyword argument.')
		else:
			app_name = kwargs['app_name']
			return """{% extends "base.html" %}
{% block content %}
  <p>Welcome to """ + app_name + """!</p>
{% endblock %}"""
	elif filename == '404_template':
		return """{% extends "base.html" %}
{% block title %} - Page Not Found{% endblock %}
{% block content %}
  <h1>Page Not Found</h1>
  <p><a href="{{ url_for('index') }}">home</a></p>
{% endblock %}"""
	else:
		raise Exception('No template found with that name.')

if __name__ == "__main__":
	main()
