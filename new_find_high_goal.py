import sys
import numpy as np
import cv2
import argparse 
import imutils
from networktables import NetworkTable
import logging

# Change path/webcam if needed
#image = cv2.imread("/home/alexl/Pictures/RealFullField/260.jpg")
cap = cv2.VideoCapture(1)
if not cap.isOpened():
	print "Video could not be opened"
record = True
outputName = 'output' + '.mp4'

logging.basicConfig(level=logging.DEBUG)

ip = sys.arg[1]

NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

pi = NetworkTable.getTable('RaspberryPi')

while True:
	ret, image = cap.read()

	# Define ranges
	UPPER_BOUND = np.array([180, 255, 255], np.uint8) 
	LOWER_BOUND = np.array([40, 195, 124], np.uint8)

	# Convert image to HSV
	hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	# Filter out everything that isn't green	
	filter_image = cv2.inRange(hsv_image, LOWER_BOUND, UPPER_BOUND)

	# Find contours in the image 
	contours, hierarchy = cv2.findContours(filter_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	# print "Before area filter, found", len(contours), " contours."
	contours = sorted(contours, key = cv2.contourArea, reverse = True)[:3]
	# print "After area filter, found", len(contours), " contours."

	goalContour = None 

	# Filter out contours on aspect ratio and max width/height
	for cnt in contours:
		rect = cv2.boundingRect(cnt)
		x,y,w,h = rect
		aspectRatio = float (w)/h
		#cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255),3 )
		if (aspectRatio > 1.1) and (w < 1000) and (h < 1000): 
			goalContour = True
			print "Found high goal."
			print cv2.contourArea(cnt)
			break

	cv2.drawContours(image, cnt, -1, (0, 0, 255), 3)
	try: 
		print('goalArea:', pi.getNumber('goalArea'))
	except KeyError:
		print('goalArea: N/A')

	pi.putNumber(cv2.contourArea(cnt))
	# TODO: Include center x/y values, width and height

	# Show the resulting image
	cv2.imshow('Target detected', image)	
	if cv2.waitKey(1) & 0xFF == ord ('q'):
		break

cap.release()
cv2.destroyAllWindows()
