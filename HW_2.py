import RPi.GPIO as GPIO
import time

l = {"g": 2, "y": 3, "r": 4}
r = {"g": 22, "y": 27, "r": 17}
gpios = [26,19,13,6,12,16,20,21]

numboard = [[0,1,1,1,0,1,1,1],
            [0,0,0,1,0,1,0,0],
            [1,0,1,1,0,0,1,1],
            [1,0,1,1,0,1,1,0],
            [1,1,0,1,0,1,0,0],
            [1,1,1,0,0,1,1,0],
            [1,1,1,0,0,1,1,1],
            [0,0,1,1,0,1,0,0],
            [1,1,1,1,0,1,1,1],
            [1,1,1,1,0,1,0,0],
            [0,0,0,0,0,0,0,0]]
def main():
    GPIO.setmode(GPIO.BCM)
    
    for key, value in l.items():
        GPIO.setup(value, GPIO.OUT)
        GPIO.output(value, False)
    for key, value in r.items():
        GPIO.setup(value, GPIO.OUT)
        GPIO.output(value, False)
    for i in gpios:
        GPIO.setup(i, GPIO.OUT)
    setNumber(10)
    try:
        gside = l
        rside = r
        while True:
            GPIO.output(rside["r"], True)
            GPIO.output(gside["r"], True)
            time.sleep(1)
            GPIO.output(gside["r"], False)
            GPIO.output(gside["g"], True)
            
            time.sleep(10)
            
            GPIO.output(gside["g"], False)
            for i in range(5,0,-1):
                setNumber(i)
                GPIO.output(gside["y"], True)
                time.sleep(0.5)
                GPIO.output(gside["y"], False)
                time.sleep(0.5)
            setNumber(10)
            tmp = gside
            gside = rside
            rside = tmp
    except KeyboardInterrupt:
        GPIO.cleanup()
def setNumber(num):
    for i in range(0,len(gpios)):
        GPIO.output(gpios[i], numboard[num][i])
main()
