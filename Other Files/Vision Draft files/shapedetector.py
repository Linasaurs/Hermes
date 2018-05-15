# import the necessary packages
import cv2

class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):

		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		#print (len(approx))


		if len(approx) == 10:
			shape = "5-point star"


		elif len(approx) == 8:
			shape = "4-point star"
	
		else:
			shape = "No Shape"
			
		edges = len(approx)
		#print shape
		#print len(approx)
		# return the name of the shape
		return shape, edges
