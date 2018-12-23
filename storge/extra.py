import socket
import threading
import sys
import time
import RPi.GPIO as GPIO
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
tempGPIO = 2

def main():
    GPIO.setmode(GPIO.BCM)
    
    sockThread = SocketThread()
    sockThread.setDaemon(True)
    sockThread.start()
        
    try:
        while(True):
            time.sleep(10)
    except KeyboardInterrupt:
        sockThread.stop()
        exit()

class SocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = "192.168.2.4"#socket.gethostbyname(socket.gethostname())
        self.port = 8089
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
        
        for ct in self.threads:
            ct.stop()
        self.sock.close()
            
class ConnectThread (threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    def run(self):
        self.running = True
        try:
            while self.running:
                humi, temp = Adafruit_DHT.read_retry(sensor, tempGPIO)
                self.conn.send((str(temp)+"\n").encode())
                time.sleep(1)
        except socket.error:
            print("Disconnect", self.addr)
            self.stop()
    def stop(self):
        self.running = False
        #self.conn.close()

main()