from flask import Flask
from flask_sockets import Sockets
import logging
import base64, json, logging, socket, select

UPLOAD_FOLDER = '/home/stelzer/flask/1'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 160 * 1024 * 1024
app.logger.setLevel(logging.DEBUG)

sockets = Sockets(app)
