import os
import binascii
import argparse
from settings import *

#---------------------------------------------------------------------
# Helper functions
#---------------------------------------------------------------------

def enum(**enums):
	return type('Enum', (), enums)

AppTypes = enum(BASIC=1, LARGE=2, ANGULAR=3)

def get_filemap(app_type, app_name):
	if app_type == AppTypes.BASIC:
		filemap = {
			'dirs': [
				'static/css',
				'static/img',
				'static/js',
				'templates',
			],
			'remote_files': [
				(bootstrap_css_url, 'static/css/bootstrap.css'),
				(bootstrap_responsive_css_url, 'static/css/bootstrap-responsive.css'),
				(bootstrap_js_url, 'static/js/bootstrap.js'),
				(bootstrap_js_min_url, 'static/js/bootstrap.min.js'),
				(jquery_url, 'static/js/jquery.js'),
				(jquery_min_url, 'static/js/jquery.min.js'),
				(favicon_url, 'static/img/favicon.ico'),
			],
			'local_files': [
				('README.md', 'README.md'),
				('.gitignore', '.gitignore'),
				('Procfile', 'Procfile'),
				('basic_app/app.py', 'app.py'),
				('templates/base.html', 'templates/base.html'),
				('templates/index.html', 'templates/index.html'),
				('templates/404.html', 'templates/404.html'),
				('templates/about.html', 'templates/about.html'),
				('static/css/main.css', 'static/css/main.css'),
			],
		}
		return filemap
	elif app_type == AppTypes.LARGE:
		filemap = {
			'dirs': [
				app_name,
				app_name + '/static/css',
				app_name + '/static/img',
				app_name + '/static/js',
				app_name + '/templates',
			],
			'remote_files': [
				(bootstrap_css_url, app_name + '/static/css/bootstrap.css'),
				(bootstrap_responsive_css_url, app_name + '/static/css/bootstrap-responsive.css'),
				(bootstrap_js_url, app_name + '/static/js/bootstrap.js'),
				(bootstrap_js_min_url, app_name + '/static/js/bootstrap.min.js'),
				(jquery_url, app_name + '/static/js/jquery.js'),
				(jquery_min_url, app_name + '/static/js/jquery.min.js'),
				(favicon_url, app_name + '/static/img/favicon.ico'),
			],
			'local_files': [
				('README.md', 'README.md'),
				('.gitignore', '.gitignore'),
				('Procfile', 'Procfile'),
				('large_app/runserver.py', 'runserver.py'),
				('large_app/__init__.py', app_name + '/__init__.py'),
				('large_app/core.py', app_name + '/core.py'),
				('large_app/models.py', app_name + '/models.py'),
				('large_app/settings.py', app_name + '/settings.py'),
				('large_app/controllers.py', app_name + '/controllers.py'),
				('templates/base.html', app_name + '/templates/base.html'),
				('templates/index.html', app_name + '/templates/index.html'),
				('templates/about.html', app_name + '/templates/about.html'),
				('templates/404.html', app_name + '/templates/404.html'),
				('static/css/main.css', app_name + '/static/css/main.css'),
			],
		}
		return filemap
	elif app_type == AppTypes.ANGULAR:
		filemap = {
			'dirs': [
				app_name,
				app_name + '/static/css',
				app_name + '/static/img',
				app_name + '/static/js',
				app_name + '/static/lib',
				app_name + '/static/lib/angular',
				app_name + '/static/lib/jquery',
				app_name + '/static/lib/bootstrap',
				app_name + '/static/partials',
				app_name + '/templates',
			],
			'remote_files': [
				(bootstrap_css_url, app_name + '/static/css/bootstrap.css'),
				(bootstrap_responsive_css_url, app_name + '/static/css/bootstrap-responsive.css'),
				(favicon_url, app_name + '/static/img/favicon.ico'),
				(bootstrap_js_url, app_name + '/static/lib/bootstrap/bootstrap.js'),
				(bootstrap_js_min_url, app_name + '/static/lib/bootstrap/bootstrap.min.js'),
				(jquery_url, app_name + '/static/lib/jquery/jquery.js'),
				(jquery_min_url, app_name + '/static/lib/jquery/jquery.min.js'),
				(angularjs_url, app_name + '/static/lib/angular/angular.js'),
				(angularjs_resource_url, app_name + '/static/lib/angular/angular-resource.js'),
				(angularjs_min_url, app_name + '/static/lib/angular/angular.min.js'),
				(angularjs_resource_min_url, app_name + '/static/lib/angular/angular-resource.min.js'),
			],
			'local_files': [
				('README.md', 'README.md'),
				('.gitignore', '.gitignore'),
				('Procfile', 'Procfile'),
				('angular_app/runserver.py', 'runserver.py'),
				('angular_app/manage.py', 'manage.py'),
				('angular_app/__init__.py', app_name + '/__init__.py'),
				('angular_app/core.py', app_name + '/core.py'),
				('angular_app/models.py', app_name + '/models.py'),
				('angular_app/settings.py', app_name + '/settings.py'),
				('angular_app/controllers.py', app_name + '/controllers.py'),
				('angular_app/index.html', app_name + '/templates/index.html'),
				('angular_app/404.html', app_name + '/templates/404.html'),
				('static/css/main.css', app_name + '/static/css/main.css'),
				('angular_app/app.js', app_name + '/static/js/app.js'),
				('angular_app/controllers.js', app_name + '/static/js/controllers.js'),
				('angular_app/services.js', app_name + '/static/js/services.js'),
				('angular_app/about.html', app_name + '/static/partials/about.html'),
				('angular_app/landing.html', app_name + '/static/partials/landing.html'),
			],
		}
		return filemap
	else:
		raise Exception('That app type is not supported!')

def random_binascii(n):
	return binascii.b2a_hex(os.urandom(n))

def make_replacements(filedata, replacements):

	for replacement in replacements:
		filedata = filedata.replace(replacement[0], replacement[1])

	return filedata

def git_add_and_commit(message):
	os.system('git add .')
	os.system('git commit -m "' + message + '"')

def configure_github(github_user, github_repo):
	os.system('git remote add origin https://github.com/' + github_user + '/' + github_repo + '.git')

def configure_heroku(heroku_app):
	os.system('heroku create --stack cedar')
	os.system('heroku apps:rename ' + heroku_app)

def configure_virtualenvwrapper(app_name, virtualenvwrapper_path):
	os.system('source ' + virtualenvwrapper_path + '; mkvirtualenv ' + app_name + '; workon ' + app_name + '; sudo pip install ' + packages_to_pip_install + '; pip freeze > requirements.txt')

def configure_virtualenv(app_name):
	os.system('virtualenv venv --distribute; source venv/bin/activate; sudo pip install ' + packages_to_pip_install + '; pip freeze > requirements.txt')

def make_dirs(dirs):
	for d in dirs:
		os.makedirs(d)

def curl_files(files):
	for f in files:
		src_url = f[0]
		dest_name = f[1]
		os.system('curl ' + src_url + ' > ' + dest_name)

#---------------------------------------------------------------------
# App creator
#---------------------------------------------------------------------

class AppCreator(object):

	def __init__(self, app_name, app_type):
		self.app_name = app_name
		self.app_type = app_type

		if app_type == AppTypes.LARGE:
			self.runserver_filename = 'runserver'
		elif app_type == AppTypes.ANGULAR:
			self.runserver_filename = 'runserver'
		else:
			self.runserver_filename = 'app'

		self.resource_path = '../resources/'
		self.destination_path = './'

	def init_app(self):
		os.mkdir(self.app_name)
		os.chdir(self.app_name)
		os.system('git init')

	def build_app(self):
		#filenames = ['README.md', '.gitignore', 'Procfile']
		#self.create_files(filenames, '')

		filemap = get_filemap(self.app_type, self.app_name)

		for d in filemap['dirs']:
			os.makedirs(d)
		for fd in filemap['local_files']:
			with open(self.destination_path + fd[1], 'w') as f:
				filedata = self.render_filedata(fd[0], '')
				f.write(filedata)
		for fd in filemap['remote_files']:
			os.system('curl ' + fd[0] + ' > ' + fd[1])

	def load_resource(self, filename, resource_dir):
		filepath = self.resource_path + resource_dir + filename
		try:
			with open(filepath, 'r') as f:
				filedata = f.read()
		except:
			print filepath
			raise Exception('No template found with that name.')
		else:
			return filedata

	def render_filedata(self, filename, resource_dir):

		replacements = [
			('[[SECRET_KEY]]', random_binascii(24)),
			('[[APP_NAME]]', self.app_name),
			('[[RUNSERVER_FILENAME]]', self.runserver_filename)
		]

		filedata = self.load_resource(filename, resource_dir)
		filedata = make_replacements(filedata, replacements)
		return filedata

#---------------------------------------------------------------------
# Main
#---------------------------------------------------------------------

def main():
	# parse arguments
	parser = argparse.ArgumentParser(description='Autogenerate a Flask app')
	parser.add_argument('appname', help='the name of the app to be created')
	parser.add_argument('--githubrepo', dest='github_repo', help='the name of the remote github repo that will be hosting the app')
	parser.add_argument('--herokuapp', dest='heroku_app', help='the name that the heroku app will be renamed to if it has not yet been taken')
	parser.add_argument('--venvname', dest='virtualenv_name', help='the name of the virtualenv for the app')
	parser.add_argument('--push', dest='push', help='automatically push to github and heroku when app has been created', action='store_true')
	parser.add_argument('--large', dest='app_type', action='store_const', const=AppTypes.LARGE)
	parser.add_argument('--angular', dest='app_type', action='store_const', const=AppTypes.ANGULAR)
	args = parser.parse_args()

	# take in additional arguments from settings
	args.github_user = github_user
	args.virtualenvwrapper_path = virtualenvwrapper_path

	# create app files
	if args.app_type:
		app_creator = AppCreator(args.appname, args.app_type)
	else:
		app_creator = AppCreator(args.appname, AppTypes.BASIC)
		
	print ''
	app_creator.init_app()
	print ''
	app_creator.build_app()
	print '\n'

	if args.app_type == AppTypes.ANGULAR:
		os.system('python manage.py create_db')
		print 'Creating db...\n'

	# configure github
	if args.github_user and args.github_repo:
		configure_github(args.github_user, args.github_repo)

	# configure heroku
	if args.heroku_app:
		configure_heroku(args.heroku_app)

	# configure virtualenv
	if args.virtualenv_name:
		if args.virtualenvwrapper_path:
			configure_virtualenvwrapper(args.virtualenv_name, args.virtualenvwrapper_path)
		else:
			configure_virtualenv(args.virtualenv_name)

	# commit all files
	git_add_and_commit('first commit')

	# push to github and heroku
	if args.push:
		if args.github_user and args.github_repo:
			os.system('git push origin master')
		if args.heroku_app:
			os.system('git push heroku master; heroku open')

	print "\nYour app has been created!\n"

if __name__ == "__main__":
	main()
