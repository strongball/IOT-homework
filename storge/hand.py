import cv2
import numpy as np
import time
class WedCam():
	def __init__(self):
		self.cap = cv2.VideoCapture(0)
		self.handSize = 70
	def get_frame(self):
		sucess = False
		while not sucess:
			sucess, frame = self.cap.read()
		frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray, (49,49),0)
		ret, binary = cv2.threshold(blur,120,255,cv2.THRESH_BINARY)
		_,contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		maxArea = 0
		maxC = None
		for c in contours:
			area = cv2.contourArea(c)
			if area > maxArea:
				maxArea = area
				maxC = c
		if maxC is None:
			raise "Error"
			return
		hull = cv2.convexHull(maxC)
		moments = cv2.moments(maxC)
		if moments['m00'] != 0:
			cx = int(moments["m10"]/moments['m00'])
			cy = int(moments["m01"]/moments['m00'])
		cent = (cx, cy)
		cv2.circle(frame, cent, self.handSize, [255,0,255], 2)

		maxC = cv2.approxPolyDP(maxC,0.03*cv2.arcLength(maxC, True),True)
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
		return  hole
if __name__ == '__main__':
	w = WedCam()
	timecount = 0
	handArray = []
	while True:
		timecount += 1
		try:
			handArray.append(w.get_frame())
		except:
			pass
		if cv2.waitKey(1) == 27: 
			break
		
		if timecount == 10:
			print(np.array(handArray).mean())
			timecount = 0
			handArray = []			
		time.sleep(0.1)
