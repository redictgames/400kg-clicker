from object_detection import *
from pyautogui import *
from PIL import ImageGrab
import win32api, win32con
import multiprocessing
import json


class Window(object):

	def __init__(self, name):
		self.name = name
		if name == "normal":
			self.pad_x = 334
			self.pad_y = 335
			self.box = (self.pad_x,self.pad_y,(self.pad_x+528), (self.pad_y+450))
		if name == "training":
			self.pad_x = 339
			self.pad_y = 401
			self.box = (self.pad_x,self.pad_y,(self.pad_x+400), (self.pad_y+400))

	def getScreenshot(self):
		return ImageGrab.grab(self.box).save("temp.png", 'PNG')

	def detectObjects(self):
		return fnd.SimpleObject("temp.png")

	def leftClick():
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
		time.sleep(.1)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
		print "Click."          #completely optional. But nice for debugging purposes.	

	def mousePos(self, x,y):
		win32api.SetCursorPos((x,y))


class Game:

	def __init__(self):
		self.objects = []

	def startGame(self):
		start_coord = locateCenterOnScreen("start.png")
		click(start_coord)

	def vecdistance(self,box):
		return ((box[1]-box[3])**2 + (box[0] - box[2])**2)**0.5

	def CropObject(self, coords):
		image = Image.open("temp.png")
		cropped_image = []
		for i in coords:
			cropped_image += [image.crop(coords)]
		return cropped_image

	def saveMidlet(self, crop):
		for i in range(len(crop)):
			crop[i].save("crop/" + str(i) + ".png")

	def mainloop(self):
		self.startGame()
		while True:
			screen = win.getScreenshot()
			defcoord = win.detectObjects()
			for i in defcoord:
				try:
					dif_x1 = (defcoord[i][2] - defcoord[i][0])/2
					dif_y1 = (defcoord[i][3] - defcoord[i][1])/2
					x1 = defcoord[i][0] + dif_x1 + win.pad_x
					y1 = defcoord[i][1] + dif_y1 + win.pad_y
					dif_x2 = (defcoord[i+1][2] - defcoord[i][0])/2
					dif_y2 = (defcoord[i+1][3] - defcoord[i][1])/2
					x2 = defcoord[i+1][0] + dif_x2 + win.pad_x
					y2 = defcoord[i+1][1] + dif_y2 + win.pad_y
					box = (x1,y1,x2,y2)
					distance = vecdistance(box)
					print(distance)
					#moveTo(x1,y1, 0.11)
					#print(pixel(x,y))
					if pixel(x1,y1)[2] > 120:
						click()
				except:
					try:
						dif_x1 = (defcoord[i][2] - defcoord[i][0])/2
						dif_y1 = (defcoord[i][3] - defcoord[i][1])/2
						x1 = defcoord[i][0] + dif_x1 + win.pad_x
						y1 = defcoord[i][1] + dif_y1 + win.pad_y
						if pixel(x1,y1)[2] > 120:
							click((x1,y1))				
					except:
						pass

				defcoord = win.detectObjects()


win = Window("normal")
game = Game()

if __name__ == "__main__":
	game.mainloop()
