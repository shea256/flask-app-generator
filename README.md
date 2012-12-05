# How to autogenerate Flask apps

First, make sure you have python, pip, git, the heroku toolbelt, virtualenv, and virtualenvwrapper.

To create a Flask app with hosting on github and heroku:

	python generator.py --githubuser=<githubuser> create APP_NAME

Options:

+ --githubuser=
+ --githubproject=
+ --herokuapp=
+ --novirtualenvwrapper
+ --useexistingherokuapp

To add a Facebook login system to your app:

	sudo python generator.py addon <app_dir> fblogin <fb_appid> <fb_appsecret> <deployment_url>

To store your Facebook user data in mongodb:

	python generator.py addon <app_dir> mongodb_for_fblogin <db_name> <db_user> <db_pw> <db_hostaddr>

More apps coming soon.