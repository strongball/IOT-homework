import RPi.GPIO as GPIO
import time
import socket
import threading

GPIO2 = 2
def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(GPIO2, GPIO.OUT)

	sockThread = SocketThread()
	sockThread.setDaemon(True)
	sockThread.start()
	try:
		while(True):
			time.sleep(10)
	except KeyboardInterrupt:
		print("get")
		sockThread.stop()
		GPIO.cleanup()
		exit()

class SocketThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.ip = "192.168.2.4"#socket.gethostbyname(socket.gethostname())
		self.port = 8088
		self.threads = []

	def run(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind( (self.ip, self.port) )
		self.sock.listen(5)
		self.running = True
		print('Server start at: %s:%s' %(self.ip, self.port))
		while self.running:
			try:
				conn, addr = self.sock.accept()
				print ('Connected by ', addr)
				ct = ConnectThread(conn, addr)
				ct.setDaemon(True)
				self.threads.append(ct)
				ct.start()
			except socket.error:
				pass
		for ct in self.threads:
			ct.stop()
		print("Sock stop")
		
	def stop(self):
		self.running = False
		self.sock.close()

class ConnectThread (threading.Thread):
	def __init__(self, conn, addr):
		threading.Thread.__init__(self)
		self.conn = conn
		self.addr = addr
	def run(self):
		self.running = True
		try:
			self.conn.send("Hello\n".encode())
			while self.running:
				data = self.conn.recv(1024).decode()
				print ("Get: "+data)
				if (data == "open\r\n"):
					print("op")
					GPIO.output(GPIO2, True)
				else:
					GPIO.output(GPIO2, False)
		except socket.error:
			print("Disconnect", self.addr)

if __name__=="__main__":
	main()