import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
#GPIO.setup(33, GPIO.OUT)
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO.output(33,GPIO.LOW)

while 1:
    if GPIO.input(31):
        print("jaig31")
    else:
        print("LOU31")
    time.sleep(0.5)


    if GPIO.input(33):
        print("jaig33")
    else:
        print("LOU33")
    time.sleep(0.5)

    print("\n")