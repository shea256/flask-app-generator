import os
import binascii
import argparse
from settings import *

# create enums
def enum(**enums):
	return type('Enum', (), enums)

App_types = enum(BASIC=1, LARGE=2)


class AppCreator(object):

	def __init__(self, app_name, app_type):
		self.app_name = app_name
		self.app_type = app_type

		self.resource_path = '../resources/'
		self.destination_path = ''

	def create_app(self):
		self.initialize_app()
		
		if self.app_type == App_types.BASIC:
			self.create_basic_app_files()
		elif self.app_type == App_types.LARGE:
			self.create_large_app_files()

	def initialize_app(self):
		os.mkdir(self.app_name)
		os.chdir(self.app_name)
		os.system('git init')

		filenames = ['README.md', '.gitignore', 'Procfile']
		self.create_files(filenames, '')

	def create_basic_app_files(self):
		# create python files
		filenames = ['app.py']
		self.create_files(filenames, 'basic_app/')

		self.create_template_files()
		
		self.grab_static_files()

	def create_large_app_files(self):
		filenames = ['runserver.py']
		self.create_files(filenames, 'large_app/')

		app_folder = 'application'
		os.mkdir(app_folder)
		self.destination_path = app_folder + '/'

		filenames = ['__init__.py', 'controllers.py', 'core.py',
			'models.py', 'settings.py']
		self.create_files(filenames, 'large_app/')

		self.create_template_files()
		
		self.grab_static_files()

	def create_files(self, filenames, resource_dir, dest_dir=''):
		for filename in filenames:
			with open(self.destination_path + dest_dir + filename, 'w') as f:
				filedata = self.render_filedata(filename, resource_dir)
				f.write(filedata)

	def create_template_files(self):
		os.mkdir(self.destination_path + 'templates')
		filenames = ['base.html', 'index.html', '404.html']
		self.create_files(filenames, 'templates/', dest_dir='templates/')

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

		if filename == 'app.py':
			filedata = self.load_resource(filename, resource_dir)
			filedata = filedata.replace("SECRET_KEY = ''", "SECRET_KEY = '" + binascii.b2a_hex(os.urandom(24)) + "'")
			return filedata
		elif filename == 'base.html':
			template_vars = """{% set site_name = \"""" + self.app_name + """\" %}"""
			filedata = template_vars + self.load_resource(filename, resource_dir)
			return filedata
		elif filename == 'README.md':
			filedata = self.load_resource(filename, resource_dir)
			filedata = filedata.replace('APPLICATION_NAME', str(self.app_name))
			return filedata
		else:
			return self.load_resource(filename, resource_dir)

	def grab_static_files(self):
		print '\n'

		os.chdir(self.destination_path)

		os.mkdir('static')
		os.makedirs('static/css')
		os.makedirs('static/js')
		os.makedirs('static/img')
		os.makedirs('static/ico')

		os.system('curl ' + bootstrap_css_url + ' > static/css/bootstrap.css')
		os.system('curl ' + bootstrap_responsive_css_url + ' > static/css/bootstrap-responsive.css')
		os.system('curl ' + bootstrap_js_url + ' > static/js/bootstrap.js')
		os.system('curl ' + bootstrap_js_min_url + ' > static/js/bootstrap.min.js')
		os.system('curl ' + jquery_url + ' > static/js/jquery.js')
		os.system('curl ' + jquery_min_url + ' > static/js/jquery.min.js')
		os.system('curl ' + favicon_url + ' > static/ico/favicon.ico')

		os.chdir('..')

		print '\n'

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

def main():
	# parse arguments
	parser = argparse.ArgumentParser(description='Autogenerate a Flask app')
	parser.add_argument('appname', help='the name of the app to be created')
	parser.add_argument('--githubrepo', dest='github_repo', help='the name of the remote github repo that will be hosting the app')
	parser.add_argument('--herokuapp', dest='heroku_app', help='the name that the heroku app will be renamed to if it has not yet been taken')
	parser.add_argument('--venvname', dest='virtualenv_name', help='the name of the virtualenv for the app')
	parser.add_argument('--push', dest='push', help='automatically push to github and heroku when app has been created', action='store_true')
	parser.add_argument('--large', dest='app_type', action='store_const', const=App_types.LARGE)
	args = parser.parse_args()

	# take in additional arguments from settings
	args.github_user = github_user
	args.virtualenvwrapper_path = virtualenvwrapper_path

	# create app files
	if not args.app_type:
		app_creator = AppCreator(args.appname, App_types.BASIC)
	else:
		app_creator = AppCreator(args.appname, args.app_type)
	print ''
	app_creator.create_app()

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

	# print success message
	print "\nYour app has been created!\n"

if __name__ == "__main__":
	main()
