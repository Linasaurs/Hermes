from PIL import Image
import pytesseract
import argparse
import cv2
import os
while 1:
	image = cv2.imread("example_02.jpg")
	#image = cv2.VideoCapture(0)
	#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	#text = pytesseract.image_to_string(gray, lang='eng', boxes=False, config = '-c language_model_penalty_non_dict_word=1 -psm=5 -oem=0')

	#cv2.imshow("gray image", image)
	text = pytesseract.image_to_string(image, lang='eng', boxes=False, config = '-c language_model_penalty_non_dict_word=1 -psm=5 -oem=0')

	print(text)

