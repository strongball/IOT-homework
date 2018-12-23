# -*- coding: utf-8 -*-
import speech_recognition as sr
from pykeyboard import PyKeyboard
# import goslate

r = sr.Recognizer()
r.energy_threshold = 4000
# gs = goslate.Goslate()
k = PyKeyboard()
while True:
	with sr.Microphone() as source:
		print("Start.....")
		audio = r.listen(source)
	try: 
		stt = r.recognize_google(audio, language="zh-tw").encode('utf-8')
		print(stt)
		# trantext = gs.translate(stt, "en")
		# print(trantext)
		if stt == "上一頁":
			k.tap_key(k.up_key)
		elif stt == "下一頁":
			k.tap_key(k.down_key)
		elif stt == "開始":
			k.tap_key(k.function_keys[5])

	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))