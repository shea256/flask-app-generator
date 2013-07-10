## Flask App Generator

Flask App Generator gives you the power to autogenerate a Flask app in seconds.

The application you generate will be laid out in one of the following formats:

+ a 'basic' app, with just a single python file as the command center
+ a 'large' app, organized as a package and separated out into distinct, specialized python files
+ a 'flask-angular' app, with a Flask API and an AngularJS front-end

Beyond app creation, you'll have the ability to automatically:

+ generate a virtual environment and install packages inside it
+ hook into a github repo
+ initialize a Heroku application and deploy to it

(it's like hackathon magic)

Enjoy, and please don't hesitate to contribute to the project or provide feedback.

### How to Use

+ Make sure you have the necessary packages installed
+ Edit settings.py
+ Run: "python generate.py [appname]"

### Required packages

+ python
+ pip
+ git

### Optional packages

+ heroku toolbelt
+ virtualenv
+ virtualenvwrapper

### Help

**usage:** generate.py [-h] [--githubrepo GITHUB_REPO] [--herokuapp HEROKU_APP]
                   [--venvname VIRTUALENV_NAME] [--push] [--large] [--angular]
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
+ --angular : organize the app as a Flask API with an angularjs front-end

