import Adafruit_DHT
import datetime, time
import json,requests
from pymongo import MongoClient
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PLTTIME =  datetime.timedelta(minutes=30)
TOKEN = "EAASXW84za5ABAK9cl58paQcrukY8TxMV4yfTfgvFUBZCZC69gK6ImpBYGTD4F4J6DzH6wip70kW6bsZCOvkyuPamZCuqfkXxi1Re8LxgiRZBDaMnltFfqYf3lnBxQTklKuoC9sgZB3so96ZCI9bSuI8qsEcDnvJJk0AeaQVbk643QZDZD"
USERID = "1092863424152383"
FILENAME = "./tmp.png"
def main():
	sensor = Adafruit_DHT.DHT11
	tempGPIO = 2
	client = MongoClient('localhost', 27017)
	db = client.test
	collect = db.detectdata
	print("Start")
	try:
		sendLock = True
		while True:
			humi, temp = Adafruit_DHT.read_retry(sensor, tempGPIO)
			ctime = datetime.datetime.now()
			if humi is not None and temp is not None:
				print(str(ctime)+" Temp={0:0.1f}*C Humi={1:0.1f}%".format(temp, humi))
				post = {
					"time": ctime,
					"temp": temp,
					"humi": humi
				}
				collect.insert_one(post)
				if humi >= 80 and sendLock:
					sendLock = False
					showPLT(collect.find({'time': {'$gte': ctime-PLTTIME, '$lt': ctime}}))
					send_fb_Image(USERID, FILENAME)
					send_fb_message(USERID, "Temp={0:0.1f}*C Humi={1:0.1f}%".format(temp, humi))
				else:
					sendLock = True
			else:
				print("Fail to get data")
			time.sleep(1) 
	except KeyboardInterrupt:
		ctime = datetime.datetime.now()
		showPLT(collect.find({'time': {'$gte': ctime-PLTTIME, '$lt': ctime}}))

def send_fb_message(to, message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(token=TOKEN)
	response_message = json.dumps({"recipient":{"id": to}, 
								   "message":{"text":message}})
	req = requests.post(post_message_url, 
						headers={"Content-Type": "application/json"}, 
						data=response_message)
	print("[{}] Reply to {}: {}".format(req.status_code, to, message))

def send_fb_Image(to, path):

	files = { "filedata" : ('filename.png', open(path, 'rb'), 'image/png')}   
	data = {
	    "recipient":'{"id":"' + to + '"}',
	    "message":'{"attachment":{"type":"image", "payload":{}}}'
	    }
	
	r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + TOKEN, files=files, data=data)
	print("[{}] Reply to {}: {}".format(r.status_code, to, path)) 

def showPLT(data):
	times = []
	temps = []
	humis = []
	for i in data:
		times.append(i["time"])
		humis.append(i["humi"])
		temps.append(i["temp"])
	# print(times)
	fig=plt.figure(figsize=(20,15))
	ax1=fig.add_subplot(111)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
	ax1.axis([times[0], times[-1], 0, 100])
	ax1.plot(times, temps,'ro-', linewidth= 5)
	ax2=ax1.twinx()
	ax2.axis([times[0], times[-1], 0, 100])
	ax1.plot(times, humis,'bo-', linewidth= 5)
	fig.savefig(FILENAME)

if __name__=="__main__":
	main()