import Adafruit_DHT
import RPi.GPIO as GPIO
import time,datetime

POWER = 6*60 # hour 
COST = 5
PAY = 5.0
outPutGPIO = 4
tempGPIO = 2
def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(outPutGPIO, GPIO.OUT)
	GPIO.output(outPutGPIO, False)

	sensor = Adafruit_DHT.DHT11
	openTime =  datetime.timedelta(hours=PAY / (POWER * COST))
	print("Start")
	print(openTime)

	try:
		isOpen = False
		while True:
			humi, temp = Adafruit_DHT.read_retry(sensor, tempGPIO)
			ctime = datetime.datetime.now()
			if humi is not None and temp is not None:
				print(str(ctime)+" Temp={0:0.1f}*C Humi={1:0.1f}%".format(temp, humi))

				if isOpen:
					if (ctime - startTime) > openTime:
						isOpen = False
						GPIO.output(outPutGPIO, False)
				else:
					if humi >= 80:
						startTime = ctime
						isOpen = True
						GPIO.output(outPutGPIO, True)
			else:
				print("Fail to get data")

			time.sleep(1) 
	except KeyboardInterrupt:
		GPIO.cleanup()

if __name__=="__main__":
	main()