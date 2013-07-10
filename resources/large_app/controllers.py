import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory

from [[APP_NAME]] import app

# app controllers
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

# special file handlers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico')

# error handlers
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
