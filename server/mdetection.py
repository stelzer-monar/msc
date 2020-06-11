# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import sys
import logging

"""
  path : directory where are/will be the frames
"""
def detectMovement(path, minarea=500): 
	logging.info("Started " + path)
	frames = 0
	# wait for the writing of the total number of frames
	while not os.path.exists(path + "/total.txt"):
		time.sleep(0.1)
  # read the total number of frames
	with open(path + "/total.txt", "r") as f:
		frames = int(f.read())

	i = 0
	while not os.path.exists(path + "/0.jpeg"):
		time.sleep(0.1)
		continue

  # initialize the first frame
	firstFrame = cv2.imread(path + "/0.jpeg", cv2.IMREAD_GRAYSCALE)
	firstFrame = imutils.resize(firstFrame, width=500)
	firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
	
  # create the file to write the frames flaged with movement
  framesFile = open(path + "/moveFrames.txt", "a+")

	# loop over the frames of the video
	while i < frames-1:
		try:
      # wait for the next frame to be written
			if not os.path.exists(path + "/" + str(i) + ".jpeg"):
				time.sleep(0.1)
				continue
      # read frame as grayscale
			frame = cv2.imread(path + "/" + str(i) + ".jpeg", cv2.IMREAD_GRAYSCALE)
			
			move=False
		 
			# resize the frame and blur it
			frame = imutils.resize(frame, width=500)
			#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			frame = cv2.GaussianBlur(frame, (21, 21), 0)
		 
			# compute the absolute difference between the current frame and
			# first frame
			frameDelta = cv2.absdiff(firstFrame, frame)
			thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		 
			# dilate the thresholded image to fill in holes, then find contours
			# on thresholded image
			thresh = cv2.dilate(thresh, None, iterations=2)
			cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
		 
			# loop over the contours
			for c in cnts:
				# if the contour is too small, ignore it
				if cv2.contourArea(c) < minarea:
					continue
		 
				move=True
			if move:
				framesFile.write(str(i) + "\n")
		except:
			pass
		i+=1
	framesFile.close()
	logging.info("Finished " + path)

if __name__ == "__main__":
	detectMovement(sys.argv[1])
