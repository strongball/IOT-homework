# -*- coding: utf-8 -*-
import cv2
import speech_recognition as sr
import RPi.GPIO as GPIO
from gtts import gTTS
import os

filename = "tmp.mp3"
led = 21

def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(led, GPIO.OUT)
	GPIO.output(led, False)
	r = sr.Recognizer()
	r.energy_threshold = 4000	
	w = WedCam()
	while True:
		if w.get_frame():
			Say("是否開啟紅色LED燈")
			with sr.Microphone() as source:
				print("Start.....")
				audio = r.listen(source)
			try: 
				stt = r.recognize_google(audio, language="zh-tw").encode('utf-8')
				print("Input: " + stt)
				if stt.find("不") >= 0:
					GPIO.output(led, False)
				if stt.find("打開") >= 0:
					GPIO.output(led, True)
			except sr.UnknownValueError:
				print("Google Speech Recognition could not understand audio")
			except sr.RequestError as e:
				print("Could not request results from Google Speech Recognition service; {0}".format(e))

		if cv2.waitKey(1) == 27: 
			break
	cv2.destroyAllWindows()
def Say(str):
	aud = gTTS(text=str, lang="zh-tw")
	aud.save(filename)
	os.system("mpg321 "+filename)

class WedCam():
	def __init__(self):
		self.cap = cv2.VideoCapture(0)
	def get_frame(self):
		tri = False
		circle = False
		sucess = False
		sucess, frame = self.cap.read()
		if not sucess:
			return False
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)  
		contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 20)

		for c in contours:
			peri = cv2.arcLength(c, True)
			if peri < 50:
				continue
			approx = cv2.approxPolyDP(c,0.1*peri,True)

			ct = len(approx)
			if ct == 3:
				cv2.drawContours(frame,[approx],-1,(0,0,255),3)
				tri = True
		if circles is not None:
			for i in circles[0,:]:
				cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
			circle = True
		cv2.imshow("img", frame)
		return tri and circle
if __name__ == '__main__':
	main()
