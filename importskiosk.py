from picamera import PiCamera
from time import gmtime, strftime
from tkinter import *
from guizero import App, PushButton, Text, Picture
from Devices import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22 import *
from Phidget22.Devices.DigitalInput import *
import requests
from send_email import Sendmail
from PIL import Image, ImageTk
import os,sys
from keyboard import *
from pygame import mixer
import PIL
from image import *
import gpiozero
from ventilator import *
from pyqrcode import *
import pypng as png
from funfacts import Funfact