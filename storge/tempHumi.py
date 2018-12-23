import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11

GPIO = 2

while True:
	ctime = time.strftime("%H:%M:%S")

	humi, temp = Adafruit_DHT.read_retry(sensor, GPIO)

	if humi is not None and temp is not None:
		print(ctime, "-> Temp={0:0.1f}*C Humi={1:0.1f}%".format(temp, humi))
	else:
		print("Fail")
	time.sleep(2) 