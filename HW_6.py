import Adafruit_DHT
import time
import json,requests
import logging
from logging.config import fileConfig

TOKEN = "EAASXW84za5ABAK9cl58paQcrukY8TxMV4yfTfgvFUBZCZC69gK6ImpBYGTD4F4J6DzH6wip70kW6bsZCOvkyuPamZCuqfkXxi1Re8LxgiRZBDaMnltFfqYf3lnBxQTklKuoC9sgZB3so96ZCI9bSuI8qsEcDnvJJk0AeaQVbk643QZDZD"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create a file handler
handler = logging.FileHandler('temperature.log')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
# create a stdout handler
shandler = logging.StreamHandler()
shandler.setLevel(logging.DEBUG)
shandler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)
logger.addHandler(shandler)

def main():
	sensor = Adafruit_DHT.DHT11
	tempGPIO = 2

	try:
		sendTime = time.time()
		while True:
			ctime = time.strftime("%H:%M:%S")

			humi, temp = Adafruit_DHT.read_retry(sensor, tempGPIO)

			if humi is not None and temp is not None:
				logger.info("Temp={0:0.1f}*C Humi={1:0.1f}%".format(temp, humi))
				if humi >= 80 and (time.time() - sendTime) > 10:
					sendTime = time.time()
					send_fb_message("1092863424152383", "Temp={0:0.1f}*C Humi={1:0.1f}%".format(temp, humi))
			else:
				logger.error("Fail to get data")
			time.sleep(1) 
	except KeyboardInterrupt:
		pass

def send_fb_message(to, message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(token=TOKEN)
	response_message = json.dumps({"recipient":{"id": to}, 
								   "message":{"text":message}})
	req = requests.post(post_message_url, 
						headers={"Content-Type": "application/json"}, 
						data=response_message)
	logger.info("[{}] Reply to {}: {}".format(req.status_code, to, message))

if __name__=="__main__":
	main()