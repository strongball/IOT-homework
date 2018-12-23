# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time, os
import RPi.GPIO as GPIO
from gtts import gTTS

filename = "tmp.mp3"
led = 21

class WedCam():
	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		self.handSize = 80
	def get_frame(self):
		sucess = False
		while not sucess:
			sucess, frame = self.cap.read()
		frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray, (37,37),0)
		ret, binary = cv2.threshold(blur,120,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		maxArea = 0
		maxC = None
		for c in contours:
			area = cv2.contourArea(c)
			if area > maxArea:
				maxArea = area
				maxC = c
		if maxC is None:
			return 0
		hull = cv2.convexHull(maxC)
		moments = cv2.moments(maxC)
		if moments['m00'] != 0:
			cx = int(moments["m10"]/moments['m00'])
			cy = int(moments["m01"]/moments['m00'])
		cent = (cx, cy)
		cv2.circle(frame, cent, self.handSize, [255,0,255], 2)

		maxC = cv2.approxPolyDP(maxC,0.01*cv2.arcLength(maxC, True),True)
		cv2.drawContours(frame,[maxC],-1,(0,0,255),3)
		cv2.drawContours(frame,[hull],-1,(0,255,255),3)
		hull = cv2.convexHull(maxC,returnPoints=False)
		defects = cv2.convexityDefects(maxC, hull)

		hole = 0
		for de in defects:
			s,e,f,d = de[0]
			start = tuple(maxC[s][0])
			end = tuple(maxC[e][0])
			far = tuple(maxC[f][0])
			# dist = cv2.pointPolygonTest(maxC, (cx, cy), True)
			if ((cent[0] - far[0]) ** 2 + (cent[1] - far[1]) ** 2) < self.handSize ** 2:
				hole += 1
			cv2.circle(frame, far, 5, [255,255,255],-1)
		cv2.imshow("img", frame)
		return hole
def Say(str):
	aud = gTTS(text=str, lang="zh-tw")
	aud.save(filename)
	os.system("mpg321 "+filename)
	print(str)

def setLed(mode):
	if mode == 3:
		GPIO.output(led, True)
		Say("兩隻手指頭，綠色LED打開了")
	elif mode == 5:
		GPIO.output(led, False)
		Say("四隻手指頭，綠色LED關閉了")
if __name__ == '__main__':
	w = WedCam()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(led, GPIO.OUT)
	GPIO.output(led, False)

	timecount = 0
	handArray = []
	while True:
		timecount += 1
		try:
			handArray.append(w.get_frame())
		except Exception as e:
			print(e)
		if cv2.waitKey(1) == 27: 
			break
		
		if timecount == 10:
			hand = np.array(handArray).mean().round()
			setLed(hand)
			timecount = 0
			handArray = []			
		time.sleep(0.1)
