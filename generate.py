import os
import binascii
import argparse
from settings import *

def git_add_and_commit(message):
	os.system('git add .')
	os.system('git commit -m "' + message + '"')

def create_files(filenames, app_name):
	for filename in filenames:
		with open(filename, 'w') as f:
			f.write(render_filedata(filename, app_name))

def create_app_files(app_name):
	if not app_name:
		raise Exception('App name required.')

	#----------------------------------------
	# create and init directory
	#----------------------------------------
	os.mkdir(app_name)
	os.chdir(app_name)
	os.system('git init')
	os.mkdir('templates')

	#----------------------------------------
	# create files
	#----------------------------------------

	filenames = ['README.md', '.gitignore', 'Procfile', 'app.py',
		'templates/base.html', 'templates/index.html', 'templates/404.html']
	create_files(filenames, app_name)

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
	os.system('source ' + virtualenvwrapper_path + '; mkvirtualenv ' + app_name + '; workon ' + app_name + '; sudo pip install ' + packages_to_pip_install + '; pip freeze > requirements.txt')

def configure_virtualenv(app_name):
	os.system('virtualenv venv --distribute; source venv/bin/activate; sudo pip install ' + packages_to_pip_install + '; pip freeze > requirements.txt')

def main():
	#----------------------------------------
	# parse arguments
	#----------------------------------------
	parser = argparse.ArgumentParser(description='Autogenerate a Flask app')
	parser.add_argument('appname', help='the name of the app to be created')
	#parser.add_argument('--githubuser', dest='github_user', help='the name of the github user that will be hosting the app')
	parser.add_argument('--githubrepo', dest='github_repo', help='the name of the remote github repo that will be hosting the app')
	parser.add_argument('--herokuapp', dest='heroku_app', help='the name that the heroku app will be renamed to if it has not yet been taken')
	parser.add_argument('--venvname', dest='virtualenv_name', help='the name of the virtualenv for the app')
	#parser.add_argument('--venvwrapperpath', dest='virtualenvwrapper_path', help='the path to the file virtualenvwrapper.sh (turns on virtualenvwrapper when specified)')
	parser.add_argument('--push', dest='push', help='automatically push to github and heroku when app has been created', action='store_true')
	args = parser.parse_args()

	args.github_user = github_user
	args.virtualenvwrapper_path = virtualenvwrapper_path

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

def load_resource(filename):
	resource_path = '../resources/'
	try:
		with open(resource_path + filename, 'r') as f:
			filedata = f.read()
	except:
		raise Exception('No template found with that name.')
	else:
		return filedata

def render_filedata(filename, app_name):
	if filename == 'app.py':
		filedata = load_resource(filename)
		filedata = filedata.replace("SECRET_KEY = ''", "SECRET_KEY = '" + binascii.b2a_hex(os.urandom(24)) + "'")
		return filedata
	elif filename == 'templates/base.html':
		template_vars = """{% set site_name = \"""" + app_name + """\" %}"""
		filedata = template_vars + load_resource(filename)
		return filedata
	elif filename == 'README.md':
		filedata = load_resource(filename)
		filedata = filedata.replace('APPLICATION_NAME', str(app_name))
		return filedata
	else:
		return load_resource(filename)

if __name__ == "__main__":
	main()
