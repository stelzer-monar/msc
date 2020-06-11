import os                                                                                                                                                                      
import time
import sys
import subprocess

imagesPath = os.getcwd() + "/img"
detectorPath = os.getcwd() + "/detector.log"
# Start api process
p1 = subprocess.Popen(['gunicorn', '-k', 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker', '-w', '4', '-b', '0.0.0.0', 'main:app'])
# Start computation process
p2 = subprocess.Popen(['python3', 'startDetection.py', imagesPath])

time.sleep(2)
# Start collecting process
p3 = subprocess.Popen(['python3', 'saveResults.py', detectorPath])

while True:
    time.sleep(60)
