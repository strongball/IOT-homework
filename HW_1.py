import RPi.GPIO as GPIO
import time

l = {"g": 2, "y": 3, "r": 4}
r = {"g": 16, "y": 20, "r": 21}

def main():
    GPIO.setmode(GPIO.BCM)
    
    for key, value in l.items():
        GPIO.setup(value, GPIO.OUT)
        GPIO.output(value, False)
    for key, value in r.items():
        GPIO.setup(value, GPIO.OUT)
        GPIO.output(value, False)
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
            for i in range(5):
                GPIO.output(gside["y"], True)
                time.sleep(0.5)
                GPIO.output(gside["y"], False)
                time.sleep(0.5)
            
            tmp = gside
            gside = rside
            rside = tmp
    except KeyboardInterrupt:
        GPIO.cleanup()
main()
