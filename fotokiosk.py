#importeert alle nodige libraries.
#de python libraries staan opgeslagen in /usr/local/lib
from importskiosk import *

#Brengt de gebruiker terug naar het begin scherm, verwijdert eventuele foto's zodat
#de gebruiker weer op een vers scherm begint.
def terug_naar_begin():
    global next
    sys.path.insert(0,"/home/pi/fotokiosk")
    os.system("rm *.png")
    raise_frame(eersteFrame)
    next = 0;
    
#start camera, en checkt of er op next is gedrukt.
#next wordt vervolgens gecheckt in take_picture()
def start_preview():
    global next
    next = 1;
    mixer.init()
    mixer.music.load('/home/pi/fotokiosk/5a3b9d71df5c31.03472295.mp3')
    mixer.music.play()
    camera.start_preview()

#maakt de foto, slaat deze op d.m.v. output.
def take_picture():
        
    #Slaat de foto op, en gebruikt hiervoor de strftime library om een uniek padnaam te creëren   
    global output
    output = strftime("/home/pi/fotokiosk/image-%d-%m %H:%M.png", gmtime())
    camera.capture(output)
    camera.stop_preview()
    
    taal = btn1.get()
    global myphoto
    #Controlleert welke taal optie is gekozen, en roept het daarbij horende frame op.
    if (taal == 1):
        #De labels en buttons voor nederlandsStapEen worden hier aangemaakt.
        myphoto = PhotoImage(file=output)
        Label(nederlandsStapEen,image=myphoto).place(x=0,y=0)
        Button(nederlandsStapEen, text='Maak foto opnieuw', command=lambda:terug_naar_begin()).place(x=0, y=400)
        Button(nederlandsStapEen, text='Bewaar foto', command=lambda:postrequest()).place(x=700, y=400)        
        raise_frame(nederlandsStapEen)
    elif (taal == 2):
        #De labels en buttons voor engelsStapEen worden hier aangemaakt.
        myphoto = PhotoImage(file=output)
        Label(engelsStapEen,image=myphoto).place(x=0,y=0)
        Button(engelsStapEen, text='Retake picture', command=lambda:terug_naar_begin()).place(x=0, y=400)
        Button(engelsStapEen, text='Save picture', command=lambda:postrequest()).place(x=700, y=400)          
        raise_frame(engelsStapEen)
    else:
        terug_naar_begin()
        
    #Wanneer er een foto wordt gemaakt controlleert dit of er wel op next is gedrukt,
    #en dus of degene niet op de knop drukt terwijl hij zichzelf nog niet zag.
    if(next != 1):
        terug_naar_begin()    

#Stuurt een postrequest naar de website, de php code op de server haalt de foto
#op de juiste manier binnen, en zet deze in de database.
def postrequest():
    global code
    url = 'http://rummens1337.nl/includes/upload.inc.php'
    files = {'file': open(output,'rb')}
    values = {'submit': 1}
    request = requests.post(url, data=values, files=files)
    code = (request.text)
    
    taal = btn1.get()
    if(taal == 1):
        Label(nederlandsStapTwee, text=code, textvariable=code).place(x=150, y=350)
        raise_frame(nederlandsStapTwee)
    elif(taal == 2):
        Label(engelsStapTwee, text=code, textvariable=code).place(x=150, y=350)
        raise_frame(engelsStapTwee)
    else:
        terug_naar_begin()
        
    
#verstuurd data naar E-mail als de gebruiker dit aangeeft.
def send_mail():
    #Roept klasse sendmail aan en geeft dit als input voor het versturen van de foto
    email = mail.get()
    taal = btn1.get()
    subject = 'Fotokiosk - Amsterdam'
    Sendmail(email,subject,output,code,taal);
    
#bekijkt de status van de digital input ( = 0 of 1 )
#als input == 1: maak foto.
def onStateChangeHandler(e, state):
    print("State %f" % state)
    if(state == 1):
        take_picture()
    return 0
    
#Print of phidget aangesloten is.
def onAttachHandler(e):
    print("Phidget attached!")
    
#Wanneer deze functie wordt aangeroepen, wordt de frame die ingevuld is, aangeroepen
def raise_frame(frame):
    frame.tkraise()

#Maakt een root window met titel aan
root = Tk()
root.title("Corendon Fotokiosk")

#variabelen die nodig zijn
nlVlag = PhotoImage(file="netherlands-Flag.jpg")
enVlag = PhotoImage(file="united-Kingdom-flag-icon.jpg")
camera = PiCamera()
camera.resolution = (800, 480)
camera.hflip = True
output= ""
btn1 = IntVar()
next = IntVar()
mail = StringVar()
code = IntVar()

#De geometry (resolutie e.d.) voor de root window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
w = 800
h = 480
x = 0
y = 0
#root.overrideredirect(1)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

'''Alle frames die nodig zijn worden hieronder aangemaakt.
Sommige labels voor frames worden pas aangemaakt bij het aanroepen
van een bepaalde functie, omdat deze anders een verkeerde waarde hebben.'''
eersteFrame = Frame(root, width=800, height=480)
nederlandsStapEen = Frame(root, width=800, height=480)
nederlandsStapTwee = Frame(root, width=800, height=480)
nederlandsStapDrie = Frame(root, width=800, height=480)
engelsStapEen = Frame(root, width=800, height=480)
engelsStapTwee = Frame(root, width=800, height=480)

#Checkt of de knop ingedrukt wordt
ch = DigitalInput()	
ch.openWaitForAttachment(500000)

ch = DigitalInput()
ch.setOnAttachHandler(onAttachHandler)
ch.setOnStateChangeHandler(onStateChangeHandler)
ch.open()

#De frames binnen de loop kan tussen worden gewisseld
for frame in (eersteFrame, nederlandsStapEen, nederlandsStapTwee, nederlandsStapDrie, engelsStapEen, engelsStapTwee):
    frame.grid(row=0, column=0, sticky='news')
    
#Alle widgets van de eerste frame (eersteFrame) en de plaatsing van de widgets
Radiobutton(eersteFrame, text="Nederlands", value=1, variable=btn1, image=nlVlag, indicatoron=0).place(x=236, y=150)
Radiobutton(eersteFrame, text="Engels", value=2, variable=btn1, image=enVlag, indicatoron=0).place(x=436, y=150)
nextKnop = Button(eersteFrame, text='Next', command=lambda:start_preview()).place(x=700, y=200)  
Label(eersteFrame, text='Choose your language').place(x=345, y=60)

#Frame nederlandsStapEen
'''De labels en buttons worden aangemaakt in "def take_picture()"'''

#Frame nederlandsStapTwee
Label(nederlandsStapTwee, text='FRAME 4')
Button(nederlandsStapTwee, text='Goto to frame 1', command=lambda:raise_frame(eersteFrame))
logo = PhotoImage(file="corendonTransparant.jpg")
Label(nederlandsStapTwee, image=logo).place(x=150, y=50)
Label(nederlandsStapTwee, text="U kunt uw foto terugvinden op www.rummens1337.nl").place(x=20, y=250)
Label(nederlandsStapTwee, text="door onderstaande code op de website in te voeren").place(x=25, y=268)
Label(nederlandsStapTwee, text="Dit is uw code:").place(x=120, y=325)
Label(nederlandsStapTwee, text="Of vul uw e-mail hieronder in:").place(x=500, y=250)
Entry(nederlandsStapTwee, width=40, textvariable=mail).place(x=475, y=300)
Button(nederlandsStapTwee, text="Verstuur!", command=send_mail).place(x=565, y=350)
Button(nederlandsStapTwee, text="Volgende", command=terug_naar_begin).place(x=400,y=200)

#Frame engelsStapEen
'''De labels en buttons worden aangemaakt in "def take_picture()"'''

#Frame engelsStapTwee
Label(engelsStapTwee, text='FRAME 4')
Button(engelsStapTwee, text='Goto to frame 1', command=lambda:raise_frame(eersteFrame))
logo = PhotoImage(file="corendonTransparant.jpg")
Label(engelsStapTwee, image=logo).place(x=150, y=50)
Label(engelsStapTwee, text="You can find your photo @ www.rummens1337.nl").place(x=20, y=250)
Label(engelsStapTwee, text="By entering your personal code").place(x=25, y=268)
Label(engelsStapTwee, text="This is your code:").place(x=120, y=325)
Label(engelsStapTwee, text="Or fill in your E-mail here:").place(x=500, y=250)
Entry(engelsStapTwee, width=40, textvariable=mail).place(x=475, y=300)
Button(engelsStapTwee, text="Send!", command=send_mail).place(x=565, y=350)
Button(engelsStapTwee, text="Next", command=terug_naar_begin).place(x=400,y=200)


raise_frame(eersteFrame)
root.mainloop()