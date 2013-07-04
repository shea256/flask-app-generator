import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory

from application import app

# Application controllers
@app.route("/")
def index():
	return render_template('index.html')

# Special file handlers
@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
