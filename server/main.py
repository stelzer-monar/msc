import os
from app import app, sockets  
from flask import Flask, request, redirect, jsonify, Response, stream_with_context, redirect, url_for, copy_current_request_context 
from flask_sockets import Sockets
from werkzeug.utils import secure_filename
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from pathlib import Path
import base64, json, logging, socket, select
import requests
import threading
import datetime
import time

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# baseDir = "/home/stelzer/flask/img/"
baseDir = os.getcwd() + "/img/"

redirect_host=""
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadFrame', methods=['POST'])
def upload_frame():
    content = request.headers
    Path(baseDir + content['id']).mkdir(parents=True, exist_ok=True)
    if content['redirect'] == "1":
        pass
    else:
        if content['frame'] == "0":
            with open(baseDir + content['id'] + "/total.txt", "w") as f:
                f.write(content['frameTotal'])
        with open(baseDir + content['id'] + "/" + content['frame'] + ".jpeg", "wb") as f:
            chunk_size = 4096
            while True:
                chunk = request.stream.read(chunk_size)
                if len(chunk) == 0:
                    resp = jsonify({'message' : 'File successfully uploaded'})
                    resp.status_code = 201
                    return resp
                f.write(chunk)

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp

if __name__ == "__main__":
    app.run()
