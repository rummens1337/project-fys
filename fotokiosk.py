#importeert alle nodige libraries.
#de python libraries staan opgeslagen in /usr/local/lib
from importskiosk import *

#Brengt de gebruiker terug naar het begin scherm, verwijdert de gebruiker gegevens zodat
#de volgende gebruiker weer op een vers scherm begint.
def terug_naar_begin():
    global next
    global mail
    global fotogemaakt
    fotogemaakt = 0
    ventilator_off()
    sys.path.insert(0,"/home/pi/fotokiosk/fotos")
    os.system("rm /home/pi/fotokiosk/fotos/*.png")
    next = 0;
    mail.set('')
    camera.stop_preview()
    mixer.music.stop()
    raise_frame(eersteFrame)
    btn1.set(5)
    print(btn1.get())
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
    
    #eerste if statement werd overgeslagen, vandaar dubbel. (backup)
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
            Button(nederlandsStapEen, height=2, width=12, text='Maak foto opnieuw', command=lambda:terug_naar_begin()).place(x=5, y=377)
            Button(nederlandsStapEen, height=2, width=9, text='Bewaar foto', command=lambda:postrequest()).place(x=700, y=377)        
            raise_frame(nederlandsStapEen)
            fotogemaakt = 1
        elif (btn1.get() == 2):
            #De labels en buttons voor engelsStapEen worden hier aangemaakt.
            myphoto = PhotoImage(file=output)
            Label(engelsStapEen,image=myphoto).place(x=0,y=0)
            Button(engelsStapEen, text='Retake picture', height=2, width=9, command=lambda:terug_naar_begin()).place(x=5, y=377)
            Button(engelsStapEen, text='Save picture', height=2, width=9, command=lambda:postrequest()).place(x=700, y=377)          
            raise_frame(engelsStapEen)
            fotogemaakt = 1
        else:
            print("LMAO")
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
        url = 'http://rummens1337.nl/includes/upload.inc.php'
        files = {'file': open(output,'rb')}
        values = {'submit': 1}
        request = requests.post(url, data=values, files=files)
        code = (request.text)
    
        taal = btn1.get()
        if(taal == 1):
            Label(nederlandsStapTwee, text=code, textvariable=code).place(x=150, y=350)
            raise_frame(nederlandsStapTwee)
            mixer.music.load('/home/pi/fotokiosk/thankyou_eng.mp3')
            mixer.music.play()
        elif(taal == 2):
            Label(engelsStapTwee, text=code, textvariable=code).place(x=150, y=350)
            raise_frame(engelsStapTwee)
        else:
            terug_naar_begin()
            
        
    
#verstuurt data naar E-mail als de gebruiker dit aangeeft.
def send_mail():
    #Roept klasse sendmail aan en geeft dit als input voor het versturen van de foto
    email = mail.get()
    taal = btn1.get()
    subject = 'Fotokiosk - Amsterdam'
    Sendmail(email,subject,output,code,taal);
    raise_frame(nederlandsStapTwee)
    
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

def annuleer_mail():
    raise_frame(nederlandsStapTwee)

#zorgt ervoor dat de ventilator standaard uit staat
ventilator_off()

#Maakt een root window met titel aan
root = Tk()
root.title("Corendon Fotokiosk")

#variabelen die nodig zijn
nlVlag = PhotoImage(file="netherlands-Flag.png")
enVlag = PhotoImage(file="united-Kingdom-flag-icon.png")
achtergrond = PhotoImage(file="achtergrond1.png")
clickme = PhotoImage(file="clickme.png")
qrcode = PhotoImage(file="qrcode3.png")
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
funfactNr = 2

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
Label(eersteFrame,image=achtergrond).place(x=0,y=0)
Radiobutton(eersteFrame, bg="#FF3333", activebackground="#FF3333", text="Nederlands", value=1, variable=btn1, image=nlVlag, indicatoron=0).place(x=236, y=260)
Radiobutton(eersteFrame, bg="#FF3333", activebackground="#FF3333", text="Engels", value=2, variable=btn1, image=enVlag, indicatoron=0).place(x=436, y=260)
nextKnop = Button(eersteFrame, bg="yellow", text='Next', command=lambda:start_preview()).place(x=700, y=320)  
Label(eersteFrame, bg="yellow", text='Choose your language').place(x=345, y=230)
Button(eersteFrame, text='Make picture',command=lambda:take_picture()).place(x=200,y=200)
Button(eersteFrame, bg="#FF3333",image=clickme,width = 100, height = 100, command=lambda:tellFunFact()).place(x=100,y=100)

#Frame nederlandsStapEen
'''De labels en buttons worden aangemaakt in "def take_picture()"'''

#Frame nederlandsStapTwee
Label(nederlandsStapTwee, image=achtergrond).place(x=0,y=0)
Button(nederlandsStapTwee, text='Go to frame 1', command=lambda:raise_frame(eersteFrame))
Label(nederlandsStapTwee, bg="#FF3333", text="U kunt uw foto terugvinden op www.rummens1337.nl").place(x=20, y=250)
Label(nederlandsStapTwee, bg="#FF3333", text="door onderstaande code op de website in te voeren").place(x=25, y=268)
Label(nederlandsStapTwee, bg="#FF3333", text="Dit is uw code:").place(x=120, y=325)
Label(nederlandsStapTwee, bg="#FF3333", text="Of vul eventueel uw e-mail in:").place(x=320, y=325)
Button(nederlandsStapTwee, bg="yellow" , text="Vul mail in!", command=lambda:raise_frame(nederlandsStapDrie)).place(x=365, y=380)
Button(nederlandsStapTwee, bg="yellow" , text="Volgende", command=terug_naar_begin).place(x=700,y=50)
Label(nederlandsStapTwee, image=qrcode).place(x=600, y=250)
#Frame engelsStapEen
'''De labels en buttons worden aangemaakt in "def take_picture()"'''

#Frame engelsStapTwee
Label(engelsStapTwee, text='FRAME 4')
Button(engelsStapTwee, text='Goto to frame 1', command=lambda:raise_frame(eersteFrame))
Label(engelsStapTwee, image=achtergrond).place(x=0, y=0)
Label(engelsStapTwee, bg="#FF3333", text="You can find your photo at www.rummens1337.nl").place(x=20, y=250)
Label(engelsStapTwee, bg="#FF3333", text="By entering your personal code").place(x=20, y=268)
Label(engelsStapTwee, bg="#FF3333", text="This is your code:").place(x=120, y=325)
Label(engelsStapTwee, bg="#FF3333", text="Or fill in your E-mail here:").place(x=320, y=325)
Button(engelsStapTwee, bg="yellow" , text="Send!", command=send_mail).place(x=365, y=380)
Button(engelsStapTwee, bg="yellow" , text="Next", command=terug_naar_begin).place(x=700,y=50)
Label(engelsStapTwee, image=qrcode).place(x=600, y=250)

#nederlandsStapDrie (Sendmail)
buttons = [
    'q','w','e','r','t','y','u','i','o','p','<-','7','8','9',
    'a','s','d','f','g','h','j','k','l','-',' ','4','5','6',
    'z','x','c','v','b','n','m','@','_','.',' ','1','2','3',
    ]

Label(nederlandsStapDrie,image=achtergrond).place(x=0,y=0)
entry = Entry(nederlandsStapDrie, textvariable=mail, width = 40)
entry.grid(row = 5, columnspan = 20)
button = Button(nederlandsStapDrie, text="Verstuur!", command=send_mail).grid(row=7, columnspan =2,column=8)
Button(nederlandsStapDrie,text="Annuleer",command=annuleer_mail).grid(row=7,columnspan=2,column= 4)
varRow = 2
varColumn = 0

for button in buttons:

    command = lambda x=button: select(x)
    if button != "Space":
        Button(nederlandsStapDrie, text = button, width = 5, bg="#000000", fg="#ffffff",
               activebackground="#ffff8f", activeforeground="#000990", relief='raised',
               padx=4, pady=4, bd=4, command=command).grid(row=varRow, column=varColumn)

        varColumn+=1
        if varColumn > 13 and varRow == 2:
            varColumn = 0
            varRow+=1
        if varColumn > 13 and varRow == 3:
            varColumn = 0
            varRow+=1

raise_frame(eersteFrame)
root.mainloop()