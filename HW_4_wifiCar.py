import socket
import threading
import signal
import sys
import time
import RPi.GPIO as GPIO

def main():
    GPIO.setmode(GPIO.BCM)
    
    sockThread = SocketThread()
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
        self.car = AutoCar()
        self.car.start()
    def run(self):
        self.running = True
        try:
            self.conn.send("Hello\n".encode())
            while self.running:
                data = self.conn.recv(1024).decode()
                print (data)
                self.car.move(data)
                self.conn.send("server received you message.\n".encode())
        except socket.error:
            print("Disconnect", self.addr)
            self.stop()
    def stop(self):
        self.running = False
        #self.conn.close()
        self.car.stop()
        
class AutoCar  (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.musicBox = LittltStar()
        self.musicBox.start()
        
        self.carGPIO = [6,13,19,26]

        self.leftLedGPIO = 20 
        self.rightLedGPIO = 21
        self.leftLed = False
        self.rightLed = False
        self.flash = True
        self.running = False
        
        for i in self.carGPIO:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, False)
        GPIO.setup(self.leftLedGPIO, GPIO.OUT)
        GPIO.setup(self.rightLedGPIO, GPIO.OUT)
        GPIO.output(self.leftLedGPIO, False)
        GPIO.output(self.rightLedGPIO, False)
        
    def run(self):
        self.running = True
        while self.running :
            GPIO.output(self.leftLedGPIO, self.leftLed)
            GPIO.output(self.rightLedGPIO, self.rightLed)
            time.sleep(0.5)
            if(self.flash):
                GPIO.output(self.leftLedGPIO, False)
                GPIO.output(self.rightLedGPIO, False)
            time.sleep(0.5)
            
    def move(self, way):
        if(way == "right"):
            self.leftLed = False
            self.rightLed = True 
            self.flash = True
            self.musicBox.play()
            self.setWheel([True, False, False, False])
        elif (way == "left"):
            self.leftLed = True
            self.rightLed = False 
            self.flash = True
            self.musicBox.play()
            self.setWheel([False, False, True, False])
        elif (way == "up"):
            self.leftLed = False
            self.rightLed = False 
            self.flash = True
            self.musicBox.play()
            self.setWheel([True, False, True, False])
        elif (way == "down"):
            self.leftLed = True
            self.rightLed = True 
            self.flash = True
            self.musicBox.play()
            self.setWheel([False, True, False, True])
        elif (way == "stop"):
            self.leftLed = True
            self.rightLed = True
            self.flash = False
            self.musicBox.mute()
            self.setWheel([False, False, False, False])
    
    def setWheel(self, mode):
        for i in range(0, len(self.carGPIO)):
            GPIO.output(self.carGPIO[i], mode[i])
    def stop(self):
        self.running = False
        self.musicBox.stop()
        
class LittltStar  (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.tone = [0, 262, 294, 330, 349, 392, 440]
        self.chord = [1,1,5,5,6,6,5,4,4,3,3,2,2,1,
                      5,5,4,4,3,3,2,5,5,4,4,3,3,2,
                      1,1,5,5,6,6,5,4,4,3,3,2,2,1]
        self.buzzGPIO = 18
        GPIO.setup(self.buzzGPIO, GPIO.OUT)
        self.buzz = GPIO.PWM(self.buzzGPIO, 440)
        self.buzz.start(60)
        
        self.playMusic = False       
        self.running = False
        
    def run(self):
        temple = 0
        self.running = True
        while self.running :
            
            if(self.playMusic):
                self.buzz.ChangeFrequency(self.tone[self.chord[temple]])
                self.buzz.ChangeDutyCycle(60)
                temple = (temple+1)%len(self.chord)
                if temple % 7 == 0:
                    time.sleep(0.9)
                else:
                    time.sleep(0.4)
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