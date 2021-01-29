import os
from app import app  
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import logging
import time
import redis
import rq
import numpy as np
from mdetection import detectMovementJob

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
baseDir = os.getcwd() + "/img/"
redisR = redis.StrictRedis()
q = rq.Queue(connection=redisR, default_timeout=9000)

redirect_host=""
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/readiness', methods=['GET'])
def readiness():
    resp = jsonify({'message' : 'UP'})
    resp.status_code = 200
    return resp

@app.route('/uploadFrame', methods=['POST'])
def upload_frame():
    headers = request.headers
    if (headers["frame"] == '0'):
      redisR.set(headers["id"] + ":total", headers["frameTotal"])
      q.enqueue(detectMovementJob, headers["id"])
    img_bytes = np.array(request.stream.read()).tostring()
    redisR.set(headers["id"] + ":" + headers["frame"], img_bytes, ex=30)
    resp = jsonify({'message' : 'File successfully uploaded'})
    resp.status_code = 201
    return resp

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
