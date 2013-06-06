# Flask App Generator

## How to Use

+ Edit settings.py
+ run "python generate.py [appname]"

## Required packages

+ python
+ pip
+ git

## Optional packages

+ heroku toolbelt
+ virtualenv
+ virtualenvwrapper

## Help

**usage:** generate.py [-h] [--githubrepo GITHUB_REPO] [--herokuapp HEROKU_APP]
                   [--venvname VIRTUALENV_NAME] [--push]
                   appname

**Autogenerate a Flask app**

**positional arguments:**
+ appname : the name of the app to be created

**optional arguments:**
+ -h, --help : show this help message and exit
+ --githubrepo GITHUB_REPO : the name of the remote github repo that will be hosting the app
+ --herokuapp HEROKU_APP : the name that the heroku app will be renamed to if it has not yet been taken
+ --venvname VIRTUALENV_NAME : the name of the virtualenv for the app
+ --push : automatically push to github and heroku when app has been created
