# How to autogenerate Flask apps

First, make sure you have python, pip, git, the heroku toolbelt, virtualenv, and virtualenvwrapper.

Next, make sure you update the virtualenvwrapper_path and hosts_path at the top of the file.

Great, now you're good to go.

To autogenerate a Flask app with twitter bootstrap design and hosting on github and heroku:

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