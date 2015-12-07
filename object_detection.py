import cv2
from PIL import Image
import pyautogui
import numpy as np

class Finder:

    def makeRectangle(self, input, output, iter = 4, a = 3, b = 3):
        try:
            image = cv2.imread(input)
        except TypeError:
            image = input

        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
        _ , thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(a,b))
        dilated = cv2.dilate(thresh,kernel,iterations = iter) # dilate
        contours , hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
        coords = {}
        # for each contour found, draw a rectangle around it on original image
        for i in range(len(contours)):
            # get rectangle bounding contour
            [x,y,w,h] = cv2.boundingRect(contours[i])

            # discard areas that are too large
            #if h>300 and w>300:
                #continue

            # discard areas that are too small
            #if h<10 or w<10:
                #print("x0: {}\ny0: {}\nx: {}\ny: {}".format(x,y,(x+w),(y+w)))
                #cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),1)
                #continue

            # draw rectangle around contour on original image
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            coords.update({i:(x,y,(x+w),(y+h))})

        # write original image with added contours to disk  
        cv2.imwrite(output, image)
        return coords

    def Harris_Corner(self, input):

        filename = input
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray,2,3,0.04)

        #result is dilated for marking the corners, not important
        #dst = cv2.dilate(dst,None)

        # Threshold for an optimal value, it may vary depending on the image.
        img[dst>0.01*dst.max()]=[0,0,255]
        cv2.imwrite("result1.png",img)
        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()



    def SimpleObject(self, object):
        img_filt = cv2.medianBlur(cv2.imread(object,0), 5)
        img_th = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        coords = {}

        for i in range(len(contours)):

            [x,y,w,h] = cv2.boundingRect(contours[i])

            if h>100 or w>100 or h<30 or w<30:
                continue

            cv2.rectangle(img_filt,(x,y),(x+w,y+h),(255,100,0),1)
            coords.update({i:(x,y,(x+w),(y+h))})

        #cv2.imwrite("result.png",img_filt)
        #cv2.imshow("img_filt", img_filt)
        #if cv2.waitKey(0) & 0xff == 27:
        #    cv2.destroyAllWindows()
        return coords


fnd = Finder()
