import numpy as np 
import cv2
import argparse
import imutils

image = cv2.imread("223.jpg")
status = "No Target"

image = imutils.resize(image, height = 640)

UPPER_BOUND = np.array([96, 255, 255], np.uint8) 
LOWER_BOUND = np.array([63, 168, 0], np.uint8)

image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
hsl_image = cv2.inRange(image, LOWER_BOUND, UPPER_BOUND)
(_, cnts, _) = cv2.findContours(hsl_image.copy(), cv2.RETR_EXTERNAL, 
	cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:2]
targetGoal = None

cv2.drawContours(image, cnts, -2, (0, 0, 255), 3)
cv2.imshow("High Goal", image)
cv2.waitKey(0)

'''
for c in cnts: 
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	
	if len(approx) == 4:
		targetGoal = approx
		break

cv2.drawContours(image, [targetGoal], -1, (0, 255, 0), 3)
cv2.imshow("High Goal", image)
cv2.waitKey(0)
'''
