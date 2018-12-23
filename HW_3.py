import RPi.GPIO as GPIO
import time

l = {"g": 2, "y": 3, "r": 4}
r = {"g": 22, "y": 27, "r": 17}
gpios = [26,19,13,6,12,16,20,21]
buzzGP = 18
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

    GPIO.setup(buzzGP, GPIO.OUT)
    buzz = GPIO.PWM(buzzGP, 440)
    buzz.start(0)
    try:
        gside = r
        rside = l
        GPIO.output(rside["r"], True)
        time.sleep(5)
        GPIO.output(gside["g"], True)
        while True:
            time.sleep(10)
            GPIO.output(gside["g"], False)
            for i in range(5,0,-1):
                setNumber(i)
                GPIO.output(gside["y"], True)
                time.sleep(0.5)
                GPIO.output(gside["y"], False)
                time.sleep(0.5)
            setNumber(10)
            GPIO.output(gside["r"], True)
            buzz.ChangeFrequency(1000)
            
            intertime = 0.4
            totaltime = 0
            while totaltime < 5:
                buzz.ChangeDutyCycle(50)
                time.sleep(intertime*0.7)
                buzz.ChangeDutyCycle(0)
                time.sleep(intertime*1.3)
                totaltime += 2*intertime
                intertime *= 0.85
            
            GPIO.output(rside["r"], False)
            GPIO.output(rside["g"], True)    
            tmp = gside
            gside = rside
            rside = tmp
    except KeyboardInterrupt:
        GPIO.cleanup()
def setNumber(num):
    for i in range(0,len(gpios)):
        GPIO.output(gpios[i], numboard[num][i])
main()
