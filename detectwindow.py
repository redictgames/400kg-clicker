import numpy as np
from PIL import ImageGrab
import cv2
from main import getObjects
import pyautogui as pi
import time

while(True):
	printscreen_pil =  ImageGrab.grab()
	printscreen_numpy = np.asarray(printscreen_pil)[:,:,::-1].copy()
	circles = getObjects(printscreen_numpy)
	for i in circles:
		pi.click((int(i[0]), int(i[1])))

	#time.sleep(0.05)