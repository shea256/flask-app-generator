import os
import json
from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for

app = Flask(__name__)

app.config.from_object('[[APP_NAME]].settings')

import [[APP_NAME]].core
import [[APP_NAME]].models
import [[APP_NAME]].controllers

