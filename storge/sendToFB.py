import json
import requests
import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates

FILENAME = "./tmp.jpg"
TOKEN = "EAASXW84za5ABAK9cl58paQcrukY8TxMV4yfTfgvFUBZCZC69gK6ImpBYGTD4F4J6DzH6wip70kW6bsZCOvkyuPamZCuqfkXxi1Re8LxgiRZBDaMnltFfqYf3lnBxQTklKuoC9sgZB3so96ZCI9bSuI8qsEcDnvJJk0AeaQVbk643QZDZD"
def sendFBMessage(to, message):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(token=TOKEN)
	response_message = json.dumps({"recipient":{"id": to}, 
								   "message":{"text":message}})
	req = requests.post(post_message_url, 
						headers={"Content-Type": "application/json"}, 
						data=response_message)
	print("[{}] Reply to {}: {}".format(req.status_code, to, message))

def sendFBImage(to, path):

	files = { "filedata" : ('filename.png', open(path, 'rb'), 'image/png')}   
	data = {
		"recipient":'{"id":"' + to + '"}',
		"message":'{"attachment":{"type":"image", "payload":{}}}'
		}
	
	r = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=' + TOKEN, files=files, data=data)
	print("[{}] Reply to {}: {}".format(r.status_code, to, path)) 
def showPLT(decibels, dtimes, vibrates, vtimes):
	fig=plt.figure()
	ax1=fig.add_subplot(111)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

	ln1 = ax1.plot(dtimes, decibels,'r-', label = "decibels")
	ax1.set_ylabel('decibels')
	ax2=ax1.twinx()
	ln2 = ax2.plot(vtimes, vibrates,'b-', label = "vibrates")
	ax2.set_ylabel('vibrates')

	lns = ln1+ln2
	ax1.legend(lns, [l.get_label() for l in lns], loc = 0)

	fig.savefig(FILENAME)
	# plt.show()
if __name__ == "__main__":
	sendFBMessage("1092863424152383", "還能用嗎")
	base = datetime.datetime.now()
	date_list = [base + datetime.timedelta(seconds=x) for x in range(0, 100)]
	showPLT(np.random.randn(100), date_list, np.random.randn(100)+20, date_list)
	sendFBImage("1092863424152383", FILENAME)