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
    global output
    output = strftime("/home/pi/fotokiosk/image-%d-%m %H:%M.png", gmtime())
    #test = code.get()
    #print(test)
    print(output)
    print("take a picture")
    camera.capture(output)
    camera.stop_preview()
    taal = btn1.get()
    #print(taal)
    if taal == 1:
        raise_frame(nederlandsStapEen)
    elif taal == 2:
        raise_frame(engelsStapEen)
    else:
        terug_naar_begin()
    if(next != 1):
        terug_naar_begin()
        
def postrequest():
    global code
    #Stuurt een postrequest naar de website, de php code op de server haalt de foto
    #op de juiste manier binnen, en zet deze in de database.  
    url = 'http://rummens1337.nl/includes/upload.inc.php'
    files = {'file': open(output,'rb')}
    values = {'submit': 1}
    request = requests.post(url, data=values, files=files)
    print (request.text)
    code = (request.text)
    raise_frame(nederlandsStapTwee)
    
#verstuurd data als gebruiker klaar is
def send_mail():
    #Roept klasse sendmail aan en geeft dit als input voor het versturen van de foto
    email = mail.get()
    subject = 'Fotokiosk - Amsterdam'
    Sendmail(email,subject,output,code);
    
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

#De geometry (resolutie e.d.) voor de root window
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
w = 800
h = 480
x = 0
y = 0
#root.overrideredirect(1)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))


#Alle frames die nodig zijn worden hieronder aangemaakt
eersteFrame = Frame(root, width=800, height=480)
nederlandsStapEen = Frame(root, width=800, height=480)
nederlandsStapTwee = Frame(root, width=800, height=480)
nederlandsStapDrie = Frame(root, width=800, height=480)
engelsStapEen = Frame(root, width=800, height=480)
engelsStapTwee = Frame(root, width=800, height=480)

#variabelen die nodig zijn
btn1 = IntVar()
nlVlag = PhotoImage(file="netherlands-Flag.jpg")
enVlag = PhotoImage(file="united-Kingdom-flag-icon.jpg")
camera = PiCamera()
camera.resolution = (800, 480)
camera.hflip = True
#output = StringVar()
#foto = "/home/pi/fotokiosk/netherlands-Flag.jpg"
output= ""
print(output)
#foto = StringVar()
#foto.set("/home/pi/fotokiosk/united-Kingdom-flag-icon.jpg")
#fototest=""
#fototest = foto
#foto = output
#ket = image.open(output)
#ket.show()
#myphoto = image.load()
testvar = "/home/pi/fotokiosk/corendonTransparant.jpg" 
myphoto = PhotoImage(file=testvar)
#myphoto = PIL.Image.open("/home/pi/fotokiosk/image-21-12 11:07.png",mode='r')
#myphoto = tk.PhotoImage(file=output)
#myphoto = PhotoImage(file=output)
# get data from old image (as you already did)
#data = list(output.getdata())

# create empty new image of appropriate format
#myphoto = Image.new('RGB', (640, 480))  # e.g. ('RGB', (640, 480))

# insert saved data into the image
#myphoto.putdata(data)
next = IntVar()
mail = StringVar()
#global code
#code = StringVar()
#code = "NiceTry"
code = IntVar()

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
Label(nederlandsStapEen,image=myphoto).place(x=0,y=0)
Button(nederlandsStapEen, text='Maak foto opnieuw', command=lambda:terug_naar_begin()).place(x=0, y=400)
Button(nederlandsStapEen, text='Send dataaz', command=lambda:postrequest()).place(x=700, y=400)

#Frame nederlandsStapTwee
Label(nederlandsStapTwee, text='FRAME 4')
Button(nederlandsStapTwee, text='Goto to frame 1', command=lambda:raise_frame(eersteFrame))
logo = PhotoImage(file="corendonTransparant.jpg")
Label(nederlandsStapTwee, image=logo).place(x=150, y=50)
Label(nederlandsStapTwee, text="U kunt uw foto terugvinden op www.rummens1337.nl").place(x=20, y=250)
Label(nederlandsStapTwee, text="door onderstaande code op de website in te voeren").place(x=25, y=268)
Label(nederlandsStapTwee, text="Dit is uw code:").place(x=120, y=325)
Label(nederlandsStapTwee, text=code, textvariable=code).place(x=150, y=350)
Label(nederlandsStapTwee, text="Of vul hier uw e-mail hieronder in:").place(x=500, y=250)
Entry(nederlandsStapTwee, width=40, textvariable=mail).place(x=475, y=300)
Button(nederlandsStapTwee, text="Verstuur!", command=send_mail).place(x=565, y=350)


Label(engelsStapEen, text='Welcome to step 2')
Button(engelsStapEen, text='Go to step 3', command=lambda:raise_frame(engelsStapTwee))


raise_frame(eersteFrame)
root.mainloop()