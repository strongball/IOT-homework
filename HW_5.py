import Adafruit_DHT
import time
import threading
import RPi.GPIO as GPIO

def main():
	GPIO.setmode(GPIO.BCM)

	sensor = Adafruit_DHT.DHT11
	tempGPIO = 2

	leds = {'r':16, 'y': 20, 'g': 21}
	for key, value in leds.items():
		GPIO.setup(value, GPIO.OUT)
		GPIO.output(value, False)

	music = LittltStar()
	music.start()
	music.mute()

	try:
		while True:
			ctime = time.strftime("%H:%M:%S")

			humi, temp = Adafruit_DHT.read_retry(sensor, tempGPIO)

			if humi is not None and temp is not None:
				print(ctime, "-> Temp={0:0.1f}*C Humi={1:0.1f}%".format(temp, humi))
				for key, value in leds.items():
					GPIO.output(value, False)				
				if temp >= 31:
					GPIO.output(leds['r'], True)
					music.play()
				elif temp >=27:
					GPIO.output(leds['y'], True)
					music.mute()
				else:
					GPIO.output(leds['g'], True)
					music.mute()
			else:
				print("Fail")
			time.sleep(2) 
			pass
	except KeyboardInterrupt:
		pass
	music.stop()
	GPIO.cleanup()


class LittltStar  (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		GPIO.setmode(GPIO.BCM)
		self.tone = [0, 262, 294, 330, 349, 392, 440]
		self.chord = [5,1,5,1,5,1,5,1]
		self.buzzGPIO = 18
		GPIO.setup(self.buzzGPIO, GPIO.OUT)
		self.vol = 60
		self.buzz = GPIO.PWM(self.buzzGPIO, 440)
		self.buzz.start(self.vol)
		
		self.playMusic = False       
		self.running = False
		
	def run(self):
		temple = 0
		self.running = True
		while self.running :
			
			if(self.playMusic):
				self.buzz.ChangeFrequency(self.tone[self.chord[temple]])
				self.buzz.ChangeDutyCycle(self.vol)
				time.sleep(0.2)
				temple = (temple+1)%len(self.chord)
			else:
				time.sleep(0.4)
			self.buzz.ChangeDutyCycle(0)
			time.sleep(0.1)
			
	def play(self):
		self.playMusic = True
	def mute(self):
		self.playMusic = False
	def stop(self):
		self.running = False

main()