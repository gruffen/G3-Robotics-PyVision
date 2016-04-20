import numpy as np
import cv2
import argparse 
import imutils

#image = cv2.imread("260.jpg")

#Define ranges
UPPER_BOUND = np.array([180, 255, 255], np.uint8) 
LOWER_BOUND = np.array([40, 195, 124], np.uint8)

camera = cv2.VideoCapture()

while True:
	(grabbed, image) = camera.read()

	if not grabbed:
		break

	#Filter image based on HSV ranges 
	image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	hsv_image = cv2.inRange(image, LOWER_BOUND, UPPER_BOUND)

	(_, cnts, _) = cv2.findContours(hsv_image.copy(), cv2.RETR_EXTERNAL, 
	cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts: 
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.01 * peri, True)
		area = cv2.contourArea(c, True)
	
		x, y, w, h = cv2.boundingRect(approx)
		aspectRatio = w/h

		if area > 400 and aspectRatio >= 1:
			cv2.drawContours(image, [approx], -1, (0, 0, 255), 4)
			#store contours in an array idk how to do that
print area, aspectRatio
cv2.imshow("Pleeeease work", image)
cv2.waitKey(0)
	


