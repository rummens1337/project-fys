#importeert alle nodige libraries.
#de python libraries staan opgeslagen in /usr/local/lib
from importskiosk import *

#maakt de foto, slaat deze op d.m.v. output.
def take_picture():
    global output
    output = strftime("/home/pi/fotokiosk/image-%d-%m %H:%M.png", gmtime())    
    print("taken a picture")
    camera.capture(output)
    camera.stop_preview()
    
#bekijkt de status van de digital input ( = 0 of 1 )
#als input > 0: maak foto, stop opvragen input.
def onStateChangeHandler(e, state):
    print("State %f" % state)
    if(state == 1):
        take_picture()
        ch.close()
    return 0
    
#Print of phidget aangesloten is.
def onAttachHandler(e):
    print("Phidget attached!")
    
#waar de foto opgeslagen wordt, ook de huidige tijd wordt opgeslagen.    
output = ""

#maakt een nieuwe window met de resolutie 800 480
app = App("De Fotokiosk", 800, 480)
message = Text(app, "IT103    groep2")
new_pic = PushButton(app, take_picture, text="Nederlands")
new_pic = PushButton(app, take_picture, text="Engels")

camera = PiCamera()
camera.resolution = (800, 480)
camera.hflip = True
camera.start_preview(alpha=200)

#Dit is de input voor de knop
ch = DigitalInput()
ch.openWaitForAttachment(5000)

ch = DigitalInput()
ch.setOnAttachHandler(onAttachHandler)
ch.setOnStateChangeHandler(onStateChangeHandler)
ch.open()
#Tot hier

app.display()

url = 'http://rummens1337.nl/includes/upload.inc.php'
files = {'file': open(output,'rb')}
values = {'submit': 1}
r = requests.post(url, data=values, files=files)
print (r.text)
code = (r.text)
#Roept klasse sendmail aan en geeft dit als input voor het versturen van de foto
email = 'Gilbertrishi@gmail.com'
subject = 'Fotokiosk - Amsterdam'
sendmail(email,subject,output,code)