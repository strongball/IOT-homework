import datetime
import numpy as np
from pymongo import MongoClient

filename = "/tmp/speech.mp3"
voiceTime = datetime.timedelta(seconds=30)
faceTime = datetime.timedelta(seconds=20)

voicePower = 50
largerPower = 80
movePower = 20

def detectFace():
	return 1
def detectVoice():
	return 20
def detectMove():
	return 10

def faceDanager():
	pass
def voiceDanager():
	pass
def moveDanager():
	pass

# def Say(str):
# 	aud = gTTS(text=str, lang="zh-tw")
# 	aud.save(filename)
# 	os.system("mpg321 "+filename)
def main():
	client = MongoClient('localhost', 27017)
	db = client.babyCarriage
	collect = db.detectData

	buffer = 0
	size = 10
	faceRecoder = np.zeros(size)
	voiceRecoder = np.zeros(size)
	safeFaceTime = datetime.datetime.now()
	safeVoiceTime = datetime.datetime.now()
	try:
		while True:
			currectTime = datetime.datetime.now()
			move = detectMove()
			voice = detectVoice()
			face = detectFace()
			buffer = buffer % size
			faceRecoder[buffer] = face
			voiceRecoder[buffer] = voice			

			if faceRecoder.mean() > 0.7:
				safeFaceTime = currectTime
			else:
				if (currectTime - safeFaceTime) > faceTime:
					faceDanager()
			if voiceRecoder.mean() > 0.7 * voicePower:
				safeVoiceTime = currectTime
			else:
				if (currectTime - safeVoiceTime) > voiceTime:
					voiceDanager()


			post = {
				"time": currectTime,
				"face": face,
				"voice": voice,
				"move": move
			}
			collect.insert_one(post)
	except KeyboardInterrupt:
		pass


if __name__ == "__main__":
	main()