#importeert alle nodige libraries.
#de python libraries staan opgeslagen in /usr/local/lib
from importskiosk import *
import time

#Brengt de gebruiker terug naar het begin scherm, verwijdert de gebruiker gegevens zodat
#de volgende gebruiker weer op een vers scherm begint.
def terug_naar_begin():
    global next
    global mail
    global fotogemaakt
    raise_frame(eersteFrame)
    fotogemaakt = 0
    ventilator_off()
    sys.path.insert(0,"/home/pi/fotokiosk/fotos")
    os.system("rm /home/pi/fotokiosk/fotos/*.png")
    next = 0;
    mail.set('')
    camera.stop_preview()
    mixer.music.stop()
    btn1.set(5)
    ventilator_off()

#start camera, en checkt of er op next is gedrukt.
#next wordt vervolgens gecheckt in take_picture()
def start_preview():
    if(btn1.get() != 2 and btn1.get() != 1):
        ventilator_off()
        camera.stop_preview()
        terug_naar_begin()
        
    ventilator_on()    
    global next
    next = 1;
    mixer.init()
    mixer.music.load('/home/pi/fotokiosk/welcome_eng.mp3')
    mixer.music.play()
    camera.start_preview()
    
    #eerste if statement werd overgeslagen na 1x loop doorlopen, vandaar dubbel. (backup)
    if(btn1.get() != 2 and btn1.get() != 1):
        camera.stop_preview()
        mixer.music.stop()
        terug_naar_begin()    

#maakt de foto, slaat deze op d.m.v. output.
def take_picture():
    global output
    global next
    global fotogemaakt
    while True:
        if(fotogemaakt == 1):
            break
        #Slaat de foto op, en gebruikt hiervoor de strftime library om een uniek padnaam te creëren           
        output = strftime("/home/pi/fotokiosk/fotos/image-%d-%m %H:%M.png", gmtime())
        camera.capture(output)
        #Controlleert welke taal optie is gekozen, en roept het daarbij horende frame op.    
        global myphoto
        if (btn1.get() == 1):
            #De labels en buttons voor nederlandsStapEen worden hier aangemaakt.
            myphoto = PhotoImage(file=output)
            Label(nederlandsStapEen,image=myphoto).place(x=0,y=0)
            Button(nederlandsStapEen, image=opnieuw, height=50, width=130, highlightthickness = 0, bd = 0, text='Maak foto opnieuw', command=lambda:terug_naar_begin()).place(x=5, y=400)
            Button(nederlandsStapEen, image=bewaar, height=50, width=130, highlightthickness = 0, bd = 0, text='Bewaar foto', command=lambda:postrequest()).place(x=660, y=400)        
            raise_frame(nederlandsStapEen)
            fotogemaakt = 1
        elif (btn1.get() == 2):
            #De labels en buttons voor engelsStapEen worden hier aangemaakt.
            myphoto = PhotoImage(file=output)
            Label(engelsStapEen,image=myphoto).place(x=0,y=0)
            Button(engelsStapEen, image=opnieuwen, height=50, width=130, highlightthickness = 0, bd = 0,text='Retake picture', command=lambda:terug_naar_begin()).place(x=5, y=400)
            Button(engelsStapEen, image=bewaaren, height=50, width=130, highlightthickness = 0, bd = 0,text='Save picture', command=lambda:postrequest()).place(x=660, y=400)          
            raise_frame(engelsStapEen)
            fotogemaakt = 1
        else:
            print("EPIC FAIL")
            break
    
        ventilator_off()
        mixer.music.stop()
        camera.stop_preview()
        
        #Wanneer er een foto wordt gemaakt controlleert dit of er wel op next is gedrukt,
        #en dus of degene niet op de knop drukt terwijl hij zichzelf nog niet zag.
        if(next != 1):
            terug_naar_begin()

    #Stuurt een postrequest naar de website, de php code op de server haalt de foto
    #op de juiste manier binnen, en zet deze in de database.
    def postrequest():
        global code
        global nlVlag
        global qrcode
        url = 'http://rummens1337.nl/includes/upload.inc.php'
        files = {'file': open(output,'rb')}
        values = {'submit': 1}
        request = requests.post(url, data=values, files=files)
        code = (request.text)
        
        #maakt een QR code aan.
        big_code = pyqrcode.create('http://rummens1337.nl/uwfoto.php?code=%s' % code, error='L', version=3, mode='binary')
        big_code.png('code.png', scale=4, module_color=[0, 0, 0, 128],background=[0xff, 0xff, 0xff])   
        qrcode = PhotoImage(file="code.png")
        
        taal = btn1.get()
        #Frames voor de laatste stap worden hier aangemaakt. afhankelijk van de gekozen taal wordt wederom het juiste frame gekozen.
        #deze worden hier pas aangemaakt omdat ze anders nog geen goede waarden hebben.
        if(taal == 1):
            Label(nederlandsStapTwee, bd=0, highlightthickness="5", highlightcolor="#FFC100", highlightbackground="#FFC100", bg="yellow", height="2", width="10", text=code, textvariable=code).place(x=80, y=400)
            Label(nederlandsStapTwee,image=qrcode).place(x=635,y=315)
            raise_frame(nederlandsStapTwee)
            mixer.music.load('/home/pi/fotokiosk/thankyou_eng.mp3')
            mixer.music.play()
        elif(taal == 2):
            Label(engelsStapTwee, bd=0, highlightthickness="5", highlightcolor="#FFC100", highlightbackground="#FFC100", bg="yellow", height="2", width="10", text=code, textvariable=code).place(x=80, y=400)
            Label(engelsStapTwee,image=qrcode).place(x=635,y=315)
            raise_frame(engelsStapTwee)
            mixer.music.load('/home/pi/fotokiosk/thankyou_eng.mp3')
            mixer.music.play()
        else:
            terug_naar_begin()
            
        
    
#verstuurt data naar E-mail als de gebruiker dit aangeeft.
def send_mail():
    #Roept klasse sendmail aan en geeft dit als input voor het versturen van de foto
    email = mail.get()
    taal = btn1.get()
    subject = 'Fotokiosk - Amsterdam'
    Sendmail(email,subject,output,code,taal);
    if(taal == 1):
        raise_frame(nederlandsStapTwee)
    elif(taal == 2):
        raise_frame(engelsStapTwee)
    
#bekijkt de status van de digital input ( = 0 of 1 )
#als input == 1: maak foto.
def onStateChangeHandler(e, state):
    print("State %f" % state)
    if(state == 1):
        take_picture()
        
#wanner channel 2 open staat houdt dit bij wanneer hij van "zwartFrame" af moet.
def VoltageChangeHandler(e, voltage):
    if (voltage < 1.0):
        stopSensor()
        
def stopSensor():
    raise_frame(eersteFrame)
    ch2.close()

def startSensor():
    raise_frame(zwartFrame)
    ch2.open()
    
#Print of phidget aangesloten is.
def onAttachHandler(e):
    print("Phidget attached!")

def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))
    
#Wanneer deze functie wordt aangeroepen, wordt de frame die ingevuld is, aangeroepen
def raise_frame(frame):
    frame.tkraise()

#vertelt een funfact (audio)
def tellFunFact():
    global funfactNr
    if(funfactNr == 6):
        funfactNr = 1
        
    #roept klasse Funfact aan met funfactNr als argument    
    Funfact(funfactNr);
    funfactNr += 1

#Selecteert welke toets is ingedrukt op het keyboard.
def select(value):
    if value == "<-":
        entry.delete(len(entry.get())-1)
    else:
        entry.insert(END, value)
        
#functie gekoppeld aan terugknop van mailscherm
def annuleer_mail():
    raise_frame(nederlandsStapTwee)

#functie gekoppeld aan terugknop van mailscherm
def abort_mail():
    raise_frame(engelsStapTwee)
    

#zorgt ervoor dat de ventilator standaard uit staat
ventilator_off()

#Maakt een root window met titel aan
root = Tk()
root.title("Corendon Fotokiosk")
root.config(cursor="none")

#Alle variabelen die onder andere gebruikt worden in functies.
nlVlag = PhotoImage(file="netherlands-Flag.png")
enVlag = PhotoImage(file="united-Kingdom-flag-icon.png")
achtergrond = PhotoImage(file="achtergrond1.png")
volgende = PhotoImage(file="Nextpijl.png")
volgendenl = PhotoImage(file="Pijl.png")
bewaar = PhotoImage(file="Buttonbf.png")
opnieuw = PhotoImage(file="Button2.png")
bewaaren = PhotoImage(file="Buttonsp.png")
opnieuwen = PhotoImage(file="Buttonrp.png")
clickme = PhotoImage(file="clickme.png")
camera = PiCamera()
camera.resolution = (800, 480)
camera.hflip = True
output= ""
btn1 = IntVar()
next = IntVar()
mail = StringVar()
code = 0
fotogemaakt = 0
value = ""
funfactNr = 3

#De geometry (resolutie e.d.) voor de root window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
w = 800
h = 480
x = 0
y = 0
root.overrideredirect(1)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

'''Alle frames die nodig zijn worden hieronder aangemaakt.
Sommige labels voor frames worden pas aangemaakt bij het aanroepen
van een bepaalde functie, omdat deze anders een verkeerde waarde hebben.'''
zwartFrame= Frame(root, bg="black", width=800, height=480)
eersteFrame = Frame(root, width=800, height=480)
nederlandsStapEen = Frame(root, width=800, height=480)
nederlandsStapTwee = Frame(root, width=800, height=480)
nederlandsStapDrie = Frame(root, width=800, height=480)
engelsStapEen = Frame(root, width=800, height=480)
engelsStapTwee = Frame(root, width=800, height=480)
engelsStapDrie = Frame(root, width=800, height=480)

#Checkt of de knop ingedrukt wordt
ch = DigitalInput()	
ch.openWaitForAttachment(500000)

ch = DigitalInput()
ch.setOnAttachHandler(onAttachHandler)
ch.setOnStateChangeHandler(onStateChangeHandler)
ch.open()

#Channel voor sensor
ch2 = VoltageInput()
ch2.setDeviceSerialNumber(175632)
ch2.setChannel(2)

ch2.setOnErrorHandler(ErrorEvent)
ch2.setOnVoltageChangeHandler(VoltageChangeHandler)
ch2.open()

#De frames binnen de loop kan tussen worden gewisseld
for frame in (eersteFrame, nederlandsStapEen, nederlandsStapTwee, nederlandsStapDrie, engelsStapEen, engelsStapTwee, engelsStapDrie, zwartFrame):
    frame.grid(row=0, column=0, sticky='news')
    
#Alle widgets van de eerste frame (eersteFrame) en de plaatsing van de widgets
Label(eersteFrame,image=achtergrond).place(x=0,y=0)
Radiobutton(eersteFrame, bg="#FF3333", highlightthickness = 0, bd = 0, activebackground="#FF3333", text="Nederlands", value=1, variable=btn1, image=nlVlag, indicatoron=0).place(x=236, y=260)
Radiobutton(eersteFrame, bg="#FF3333", highlightthickness = 0, bd = 0, activebackground="#FF3333", text="Engels", value=2, variable=btn1, image=enVlag, indicatoron=0).place(x=436, y=260)
nextKnop = Button(eersteFrame, image=volgende, height=40, width=100, highlightthickness = 0, bd = 0, bg="#FF3333", text='Next', command=lambda:start_preview()).place(x=670, y=340)  
Label(eersteFrame, bg="#FF3333", fg="white", text='Choose your language').place(x=345, y=230)
#Button(eersteFrame, text='Make picture',command=lambda:take_picture()).place(x=200,y=200)
Button(eersteFrame, bg="#FF3333", image=clickme, highlightthickness = 0, bd = 0, activebackground="#FF3333", width = 100, height = 100, command=lambda:tellFunFact()).place(x=50,y=50)

#Frame nederlandsStapEen
'''De labels en buttons worden aangemaakt in "def take_picture()"'''

#Frame nederlandsStapTwee
Label(nederlandsStapTwee, image=achtergrond).place(x=0,y=0)
Button(nederlandsStapTwee, text='Go to frame 1', command=lambda:raise_frame(eersteFrame))
Label(nederlandsStapTwee, bg="#FF3333", font=("Courier", 10), fg="white", text="U kunt uw foto terugvinden op").place(x=25, y=300)
Label(nederlandsStapTwee, bg="#FF3333", font=("Courier", 10), fg="white", text="www.rummens1337.nl door onderstaande").place(x=25, y=318)
Label(nederlandsStapTwee, bg="#FF3333", font=("Courier", 10), fg="white", text="code op de website in te voeren").place(x=25, y=336)
Label(nederlandsStapTwee, bg="#FF3333", font=("Courier", 10), fg="white", text="Dit is uw code:").place(x=60, y=370)
Label(nederlandsStapTwee, bg="#FF3333", font=("Courier", 10), fg="white", text="Of vul eventueel uw e-mail in:").place(x=320, y=370)
Button(nederlandsStapTwee, bg="yellow", fg="black", text="Voer E-mail in!", command=lambda:raise_frame(nederlandsStapDrie)).place(x=370, y=400)
Button(nederlandsStapTwee, bg="#FF3333", image=volgendenl, height=40, width=100, highlightthickness = 0, bd = 0, text="Volgende", command=terug_naar_begin).place(x=670,y=250)
#Button(eersteFrame, command=lambda:raise_frame(engelsStapDrie)).place(x=100, y=100)
#nederlandsStapDrie (Sendmail)
buttons = [
    'q','w','e','r','t','y','u','i','o','p','<-','7','8','9',
    'a','s','d','f','g','h','j','k','l','-','.com','4','5','6',
    'z','x','c','v','b','n','m','@','_','.','.nl','1','2','3',
    ]

Label(nederlandsStapDrie,image=achtergrond).place(x=0,y=0)
entry = Entry(nederlandsStapDrie, textvariable=mail, width = 40)
entry.grid(row = 5, columnspan = 16)
button = Button(nederlandsStapDrie, text="Verstuur!", command=send_mail).grid(row=5, columnspan =2,column=12)
Button(nederlandsStapDrie,text="Annuleer",command=annuleer_mail).grid(row=5,columnspan=2,column= 2)
varRow = 8
varColumn = 1

#opmaak van keyboard
nederlandsStapDrie.grid_rowconfigure(1, minsize=50)
nederlandsStapDrie.grid_rowconfigure(3, minsize=170)
nederlandsStapDrie.grid_rowconfigure(6, minsize=30)
nederlandsStapDrie.grid_columnconfigure(0, minsize=15)
nederlandsStapDrie.grid_columnconfigure(15, minsize=15)

for button in buttons:

    command = lambda x=button: select(x)
    if button != "Space":
        Button(nederlandsStapDrie, text = button, width = 5, height = 2, bg="#000000", fg="#ffffff",
               activebackground="#ffff8f", activeforeground="#000990", relief='raised',
               padx=4, pady=4, bd=4, command=command).grid(row=varRow, column=varColumn)

        varColumn+=1
        if varColumn > 14 and varRow == 8:
            varColumn = 1
            varRow+=1
        if varColumn > 14 and varRow == 9:
            varColumn = 1
            varRow+=1
            
#Frame engelsStapEen
'''De labels en buttons worden aangemaakt in "def take_picture()"'''

#Frame engelsStapTwee
Label(engelsStapTwee, text='FRAME 4')
Button(engelsStapTwee, text='Goto to frame 1', command=lambda:raise_frame(eersteFrame))
Label(engelsStapTwee, image=achtergrond).place(x=0, y=0)
Label(engelsStapTwee, bg="#FF3333", fg="white", font=("Courier", 10), text="You can find your photo at").place(x=25, y=300)
Label(engelsStapTwee, bg="#FF3333", fg="white", font=("Courier", 10), text="www.rummens1337.nl by").place(x=25, y=318)
Label(engelsStapTwee, bg="#FF3333", fg="white", font=("Courier", 10), text="entering your personal code").place(x=25, y=336)
Label(engelsStapTwee, bg="#FF3333", fg="white", font=("Courier", 10), text="This is your code:").place(x=60, y=370)
Label(engelsStapTwee, bg="#FF3333", fg="white", font=("Courier", 10), text="Or fill in your E-mail below:").place(x=320, y=370)
Button(engelsStapTwee, bg="yellow", fg="black", text="Enter E-mail!", command=lambda:raise_frame(engelsStapDrie)).place(x=370, y=400)
Button(engelsStapTwee, bg="#FF3333", image=volgende, height=40, width=100, highlightthickness = 0, bd = 0, text="Next", command=terug_naar_begin).place(x=670,y=250)

#Frame engelsStapDrie
buttons_eng = [
    'q','w','e','r','t','y','u','i','o','p','<-','7','8','9',
    'a','s','d','f','g','h','j','k','l','-','.com','4','5','6',
    'z','x','c','v','b','n','m','@','_','.','.nl','1','2','3',
    ]

Label(engelsStapDrie,image=achtergrond).place(x=0,y=0)
entry = Entry(engelsStapDrie, textvariable=mail, width = 40)
entry.grid(row = 5, columnspan = 20)
button = Button(engelsStapDrie, text="Send!", command=send_mail).grid(row=5, columnspan=2,column=12)
Button(engelsStapDrie,text="Back",command=abort_mail).grid(row=5,columnspan=2,column= 2)
varRow = 8
varColumn = 1

for button in buttons_eng:

    command = lambda x=button: select(x)
    if button != "Space":
        Button(engelsStapDrie, text = button, width = 5, height = 2, bg="#000000", fg="#ffffff",
               activebackground="#ffff8f", activeforeground="#000990", relief='raised',
               padx=4, pady=4, bd=4, command=command).grid(row=varRow, column=varColumn)

        varColumn+=1
        if varColumn > 14 and varRow == 8:
            varColumn = 1
            varRow+=1
        if varColumn > 14 and varRow == 9:
            varColumn = 1
            varRow+=1
            
engelsStapDrie.grid_rowconfigure(1, minsize=50)
engelsStapDrie.grid_rowconfigure(3, minsize=170)
engelsStapDrie.grid_rowconfigure(6, minsize=30)
engelsStapDrie.grid_columnconfigure(0, minsize=15)
engelsStapDrie.grid_columnconfigure(15, minsize=15)

raise_frame(zwartFrame)
root.mainloop()