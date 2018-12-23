import RPi.GPIO as GPIO
import time

tone = [[0,0,0,0,0],
        [66,131,262,523,1046],
        [74,147,294,587,1175],
        [83,165,330,659,1318],
        [88,175,349,698,1397],
        [98,196,392,784,1568],
        [110,220,440,880,1760],
        [124,247,494,988,1976]]

playtone = [tone[0][2],tone[1][2],tone[2][2],tone[3][2],
            tone[4][2],tone[5][2],tone[6][2]]
led = [14,2,3,4,17,27,22]

chord = [1,1,5,5,6,6,5,4,4,3,3,2,2,1,
         5,5,4,4,3,3,2,5,5,4,4,3,3,2,
         1,1,5,5,6,6,5,4,4,3,3,2,2,1]
def main():
    GPIO.setmode(GPIO.BCM)

    for i in led:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, False)
    GP18 = 18
    GPIO.setup(GP18, GPIO.OUT)

    buzz = GPIO.PWM(GP18, 440)
    buzz.start(50)
    try:
        for i in range(0, len(chord)):
            c = chord[i]
            buzz.ChangeFrequency(playtone[c])
            GPIO.output(led[c], True)
            if i % 7 == 6:
                time.sleep(1)
            else:
                time.sleep(0.5)
            buzz.ChangeDutyCycle(0)
            GPIO.output(led[c], False)
            time.sleep(0.2)
            buzz.ChangeDutyCycle(50)
    except KeyboardInterrupt:
        pass
    GPIO.cleanup()
main()
