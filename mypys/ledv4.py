import appuifw
import sys
from appuifw import *
from key_codes import *
import e32, graphics, math
from httplib import (HTTPSConnection,HTTPException)
import urllib
import httplib

try:
    sys.modules['socket'] = __import__('btsocket')
except ImportError:
    pass
import socket


# create an exit handler
def quit():
    global running
    running=0
    appuifw.app.set_exit()

# set the screen size to large
appuifw.app.screen='large'

# define an initial image (white)
img=graphics.Image.open(u'c:\\data\\images\\redledfont-002.jpg')
sMessage = "   FELIZ 2018"
LETTER_HEIGHT = 144.5 
LETTER_WIDTH = 116.5 # casi
iStep = 0 
iDrawPhase = 0
ballDone = True
Mesp = {'$':(4,4), '%':(4,3), '.' : (3,0), '?':(3,1), '!':(3,2), '(':(3,3),  ')':(3,4), ':':(3,5),
        '+':(4,0), '-':(4,1), '=':(4,2)}
def getText():
    global sMessage, fileText
    try:
        f=open(fileText,'r')
        sMessage = f.read()
        #print "getText " + sMessage
        f.close()
    except:
        f=open(fileText,'w')
        f.write(sMessage)
        f.close()

def stop():
    global running
    running=0

def callback(event):
    global iCharCode
    if event['type'] == appuifw.EEventKey:
	iCharCode=event['scancode']

def getSymbol():
    global sMessage
    try:
         s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
         s.connect((HOST,PORT))
         s.sendall("GET /TickerServer/tck \r\n\r\n")
         str = u""
         print "waiting response"
         while True:
           data = s.recv(256)
           if not data:
              break
           str += data
         s.close()
         sMessage = "    " + str.upper()
    except:
        sMessage = "    Servidor fuera!".upper()


def drawLetter(iSpriteRow, iSpriteCol,  iPos, letter):  
    global iStep, LETTER_HEIGHT, LETTER_WIDTH, canvas,  ballDone 
    xPos = (LETTER_WIDTH * iPos) - iStep;
    xPos = math.floor (xPos)
    if ((xPos > 0 - LETTER_WIDTH) and (xPos < 319 + LETTER_WIDTH)):
        canvas.blit(img, source=[(iSpriteCol * LETTER_WIDTH, iSpriteRow * LETTER_HEIGHT),((iSpriteCol +1 ) * LETTER_WIDTH  , (iSpriteRow +1) * LETTER_HEIGHT)]  , target=(xPos, 0))
        ballDone = False


def handle_redraw(rect):
  global running, iStep,  ballDone, iDrawPhase
  iCounter = 0
  iCharCode = 0
  ballDone = True
  for iCounter in range(0, len(sMessage)):
        letter = sMessage[iCounter]
        iCharCode = ord(sMessage[iCounter])  
        if (iCharCode > 64 and iCharCode < 91):
            iSpriteCol = (iCharCode - 65 ) % 10
            iSpriteRow = math.floor((iCharCode - 65) / 10)
        elif (iCharCode > 47 and iCharCode < 58):
            iSpriteCol = (iCharCode - 48 ) 
            iSpriteRow = 5
        else:
            try:
               iSpriteRow = Mesp[letter][0]
               iSpriteCol = Mesp[letter][1]
            except:
               iSpriteCol = 6
               iSpriteRow = 2
               letter = " " 
        drawLetter(iSpriteRow, iSpriteCol, iCounter, letter)
        #print iCharCode,iSpriteRow, iSpriteCol
  if (ballDone):
        if (( iDrawPhase % 9 ) == 0 ):
            getSymbol()
            iDrawPhase = 0
            e32.reset_inactivity()
        iStep = 0
        iDrawPhase = iDrawPhase + 1
  else:
        iStep += 20
  

def set_accesspoint():
    apid = socket.select_access_point()
    if appuifw.query(u"Set as default access point","query") == True:
        f = open(AP,'w')
        f.write(repr(apid))
        f.close()
        appuifw.note(u"Saved default access point ", "info")
        apo = socket.access_point(apid)
        socket.set_default_access_point(apo)

def getAccessPoint():
    global apo
    print "Conectando APO"
    try:
        f=open(AP,'rb')
        setting = f.read()
        #print "defapo "  + setting
        apid = eval(setting)
        f.close()
        if not apid == None :
            apo = socket.access_point(apid)
            socket.set_default_access_point(apo)
        else:
            set_accesspoint()
    except:
        set_accesspoint()


HOST = "a.comercializa.com.co"
PORT = 8888
AP='c:\\data\\python\ap.txt'    
apo=None 
getAccessPoint() 
apo.start()

#getSymbol()
running=1
iCharCode=0
fileText = u'c:\\data\\download\\ledtext.txt'
#getText()

# define the canvas, include the redraw callback function
canvas=appuifw.Canvas(event_callback=callback,redraw_callback=handle_redraw)
# set the app.body to canvas
appuifw.app.body=canvas
canvas.clear(0x000000)
app.exit_key_handler=quit
canvas.bind(EKeyDownArrow,stop)

# create a loop to redraw the the screen again and again until the exit button is pressed
while running:
    # redraw the screen
    handle_redraw(())
    # yield needs to be here in order that key pressings can be noticed
    #e32.ao_yield()  #WAS aur test 
    e32.ao_sleep(0.1)
print "-------------------"
