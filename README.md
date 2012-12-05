
To create a Flask app with hosting on github and heroku:

	python generator.py --githubuser=<githubuser> create APP_NAME

To add a Facebook login system to your app:

	sudo python generator.py addon <app_dir> fblogin <fb_appid> <fb_appsecret> <deployment_url>

To store user data in mongodb:

	python generator.py addon <app_dir> mongodb_for_fblogin <db_name> <db_user> <db_pw> <db_hostaddr>