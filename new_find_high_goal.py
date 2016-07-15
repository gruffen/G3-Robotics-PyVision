import numpy as np
import cv2
import argparse 
import imutils

# Change path/webcam if needed
#image = cv2.imread("/home/alexl/Pictures/RealFullField/260.jpg")
cap = cv2.VideoCapture(1)

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
	contours = sorted(contours, key = cv2.contourArea, reverse = True)[:3]
	goalContour = None 

	# Draw the contours on original image
	cv2.drawContours(image, contours, -1, (0, 0, 255), 3)

	# Show the resulting image
	cv2.imshow('Image with contours', image)	
	if cv2.waitKey(1) & 0xFF == ord ('q'):
		break

cap.release()
cv2.destroyAllWindows()
