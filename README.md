# Flask App Generator

## Required packages

+ python
+ pip
+ git

## Optional packages

+ heroku toolbelt
+ virtualenv
+ virtualenvwrapper

## Help

**usage:** generate.py [-h] [--githubuser GITHUB_USER] [--githubrepo GITHUB_REPO]
                    [--herokuapp HEROKU_APP] [--venvname VIRTUALENV_NAME]
                    [--venvwrapperpath VIRTUALENVWRAPPER_PATH] [--push]
                    appname

**Autogenerate a Flask app**

**positional arguments:**
+ appname : the name of the app to be created

**optional arguments:**
+ -h, --help : show this help message and exit
+ --githubuser GITHUB_USER : the name of the github user that will be hosting the app
+ --githubrepo GITHUB_REPO : the name of the remote github repo that will be hosting the app
+ --herokuapp HEROKU_APP : the name that the heroku app will be renamed to if it has not yet been taken
+ --venvname VIRTUALENV_NAME : the name of the virtualenv for the app
+ --venvwrapperpath VIRTUALENVWRAPPER_PATH : the path to the file virtualenvwrapper.sh (turns on virtualenvwrapper when specified)
+ --push : automatically push to github and heroku when app has been created
