import RPi.GPIO as GPIO            # import RPi.GPIO module  
GPIO.setwarnings(False)            # Stopt leuke melding
GPIO.setmode(GPIO.BCM)             # BCM als mode, board kan ook. 
GPIO.setup(24, GPIO.OUT)           # set GPIO24 as an output   
    
def ventilator_off():
    GPIO.output(24, 0)
        
def ventilator_on():
    GPIO.output(24,1)
