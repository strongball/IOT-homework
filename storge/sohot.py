import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11

GPIO = 2

while True:
	ctime = time.strftime("%H:%M:%S")

	humi, temp = Adafruit_DHT.read_retry(sensor, GPIO)

	if humi is not None and temp is not None:
		heat = temp  + humi * 0.1
		print("%s -> coefficient=%0.1f Temp: %0.1f*c Humi: %0.1f%s"%(ctime, heat, temp, humi, "%"))
	else:
		print("Fail")
	time.sleep(2) 