import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response

from [[APP_NAME]] import app

# special file handlers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

# catch-all url handler
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
	return make_response(open('[[APP_NAME]]/templates/index.html').read())

