from pygame import mixer
class Funfact:
    def __init__(self,funfactNr):
        self.funfactNr = funfactNr
        if(funfactNr == 1):
            mixer.init()
            mixer.music.load('/home/pi/fotokiosk/funfact_1.mp3')
            mixer.music.play()
        if(funfactNr == 2):
            mixer.init()
            mixer.music.load('/home/pi/fotokiosk/funfact_2.mp3')
            mixer.music.play()
        if(funfactNr == 3):
            mixer.init()
            mixer.music.load('/home/pi/fotokiosk/funfact_3.mp3')
            mixer.music.play()
        if(funfactNr == 4):
            mixer.init()
            mixer.music.load('/home/pi/fotokiosk/funfact_4.mp3')
            mixer.music.play()
        if(funfactNr == 5):
            mixer.init()
            mixer.music.load('/home/pi/fotokiosk/funfact_5.mp3')
            mixer.music.play()
        if(funfactNr == 6):
            mixer.init()
            mixer.music.load('/home/pi/fotokiosk/funfact_6.mp3')
            mixer.music.play()