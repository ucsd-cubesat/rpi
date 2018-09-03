import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) 

GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

def LED(x): #temp = 1, imu = 2, server = 3, shutdown = else
    if(x == 1):
        GPIO.output(11, GPIO.HIGH)
    elif(x == 2):
        GPIO.output(13, GPIO.HIGH)
    elif(x == 3):
        GPIO.output(15, GPIO.HIGH)
    else:
	GPIO.output(11, GPIO.LOW)
    	GPIO.output(13, GPIO.LOW)
	GPIO.output(15, GPIO.LOW)  
   
