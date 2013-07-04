# Flask App Generator

With this python script, you can autogenerate a Flask application in seconds.

Additionally, you have the option of:

+ automatically generating a virtual environment and installing packages inside it
+ hooking into a github repo
+ initializing a Heroku application and deploying to it

**(it's like hackathon magic)**

The application you generate can be laid out as either a 'basic' application, with just a single python file as your command center, or a 'large' application, organized as a package and separated out into distinct, specialized python files.

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
                   [--venvname VIRTUALENV_NAME] [--push] [--large]
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
+ --large : organize the app in a way that is superior for larger applications (in the form of a package instead of a module)
