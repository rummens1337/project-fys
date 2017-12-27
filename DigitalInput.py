from Phidget22.Devices.DigitalInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *

def onStateChangeHandler(e, state):
    print("State %f" % state)
    if ("State %f" % state == 1):
        close()
    return 0

def onAttachHandler(e):
    print("Phidget attached!")
  
ch = DigitalInput()	
ch.openWaitForAttachment(5000)

ch = DigitalInput()	
ch.setOnAttachHandler(onAttachHandler)
ch.setOnStateChangeHandler(onStateChangeHandler)
ch.open()
