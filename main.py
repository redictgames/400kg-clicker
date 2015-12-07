import cv2
import numpy as np
import sys

'''
print __doc__
try:
    fn = sys.argv[1]
except:
    fn = "test.png"

# load the image, convert it to grayscale, and blur it
image = cv2.imread(fn, 1)'''

def getObjects(image):
	image = image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (3, 3), 0)
	edged = cv2.Canny(gray, 10, 250)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
	closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
	(_ ,cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	total = 0

	for c in cnts:
	# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if the approximated contour has four points, then assume that the
		# contour is a book -- a book is a rectangle and thus has four vertices
		if len(approx) == 4:
			[x,y,w,h] = cv2.boundingRect(approx)
			if w == 520 and h == 460:
				#if w == 
				cv2.drawContours(image, [approx], -1, (0, 255, 0), 4)
				image = image[y:y+h, x:x+w]
				total = True
				break

	if total:
		img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		img = cv2.medianBlur(img, 5)
		cimg = image.copy() # numpy function

		circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, 100, np.array([]), 100, 20, 1, 30)
		a, b, c = circles.shape

		border = 20

		d = []

		for i in range(b):
			if border < circles[0][i][0] < 520-border and border < circles[0][i][1] < 460-border:
			    d.append((circles[0][i][0]+x, circles[0][i][1]+y))

		return d

	else:
		print 'border was not found!'

	return []

#cv2.imshow("detected circles", cimg)
#cv2.waitKey(0)