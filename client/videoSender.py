import cv2 
import base64
import requests
import uuid
import logging
import threading
import time
import sys
import os

"""
  Singleton that breaks video into frames and hold a list of them
"""
class OnlyOne:
    class __OnlyOne:
        def __init__(self):
           self.framesList = []
           content_path = os.getcwd() + "/output.mp4"
           vidObj = cv2.VideoCapture(content_path)
           success = True
           self.length = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
           while success:
               success, image = vidObj.read()
               if success:
                   success, buffer = cv2.imencode('.jpg', image)
               self.framesList.append(buffer)
           vidObj.release()
    instance = None
    def __init__(self):
        if not OnlyOne.instance:
            OnlyOne.instance = OnlyOne.__OnlyOne()
    def __getattr__(self, name):
        return getattr(self.instance, name)

"""
  x    : video singleton holder
  tid  : thread id
  load : cloud offload frequency
"""
def sendAllFrames(x, tid, load):
    framesCount=0
    id = str(uuid.uuid4())
    startVideo = time.time()
    for buf in x.framesList: 
        start = time.time()
        r = requests.post("http://10.3.77.94:8000/uploadFrame", data=buf.tostring(), headers={'id': id, "frame" : str(framesCount), "frameTotal" : str(x.length), "redirect" : "0" if load == 0 or tid % load == 0 else "1" })
        logger.info(id + " " + str(framesCount) + " " + str(time.time()-start))
        framesCount+=1
    logger.info(id + " video " + str(time.time()-startVideo))
    
def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

"""
  usersN: number of users to be simulated
  load: cloud offload frequency
"""
def main(usersN, load) {
  content = OnlyOne()
  threadsList = []
  logging.basicConfig(filename='test' + str(usersN) + "_" + str(int(time.time())) + '.log', level=logging.INFO)
  logger = logging.getLogger(__name__)

  for i in range(int(usersN)):
      a = threading.Thread(target=sendAllFrames, args=(content, i, load)))
      threadsList.append(a)
      a.start()
}

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
