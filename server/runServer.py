import os                                                                                                                                                                      
import time
import sys
import subprocess
import signal

pros = []

def handler(signal_received, frame):
    for p in pros:
      os.killpg(os.getpgid(p.pid), signal.SIGTERM)

    sys.exit(0)

if __name__ == '__main__':
  # Tell Python to run the handler() function when SIGINT is recieved
  signal.signal(signal.SIGINT, handler)

  imagesPath = os.getcwd() + "/img"
  detectorPath = os.getcwd() + "/detector.log"
  # Start api process
  pros.append(subprocess.Popen(['gunicorn', '-k', 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker', '-w', '4', '-b', '0.0.0.0', 'main:app'], start_new_session=True))# , preexec_fn=os.setsid))
  # Start computation process
  for i in range(100):
    pros.append(subprocess.Popen(['rqworker'], start_new_session=True))#preexec_fn=os.setsid))
    #p2 = subprocess.Popen(['python3', 'startDetection.py', imagesPath]))

  time.sleep(2)
  # Start collecting process
  pros.append(subprocess.Popen(['python3', 'saveResults.py', detectorPath], start_new_session=True))#preexec_fn=os.setsid))

  while True:
      time.sleep(60)
