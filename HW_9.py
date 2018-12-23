# -*- coding: utf-8 -*-
import speech_recognition as sr
import RPi.GPIO as GPIO
from gtts import gTTS
import os

filename = "tmp.mp3"
leds = {"紅": 16, "黃": 20, "綠": 21}

def main():
	GPIO.setmode(GPIO.BCM)
	for key, value in leds.items():
		GPIO.setup(value, GPIO.OUT)
		GPIO.output(value, False)
	r = sr.Recognizer()
	r.energy_threshold = 4000	
	try:
		while True:
			with sr.Microphone() as source:
				print("Start.....")
				audio = r.listen(source)
			try: 
				stt = r.recognize_google(audio, language="zh-tw").encode('utf-8')
				print("Input: " + stt)

				action = None
				toSay = ""
				if stt.find("打開") >= 0:
					action = True
					toSay = "打開"
				elif stt.find("關閉") >= 0:
					action = False
					toSay = "關閉"

				if action is not None:
					for k, pin in leds.items():
						if stt.find(k) >= 0:
							GPIO.output(pin, action)
							Say("{}色的LED燈{}了".format(k, toSay))
			except sr.UnknownValueError:
				print("Google Speech Recognition could not understand audio")
			except sr.RequestError as e:
				print("Could not request results from Google Speech Recognition service; {0}".format(e))
	except KeyboardInterrupt:
		GPIO.cleanup()
def Say(str):
	aud = gTTS(text=str, lang="zh-tw")
	aud.save(filename)
	os.system("mpg321 "+filename)
if __name__=="__main__":
	main()