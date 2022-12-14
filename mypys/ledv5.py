#
# Screen is 240x320 pixels
# 
import appuifw
from appuifw import *
from key_codes import *
import e32, graphics, math
import sys

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
appuifw.app.screen='full'

# define an initial image (white)
img=graphics.Image.open(u'c:\\data\\images\\generatedtext-003.jpg')
sMessage = "2"
scale = 0
LETTER_HEIGHT = 250  #152 
LETTER_WIDTH = 160 #100
HEIGHT = 240
iStep = 0 
X= math.floor( (320 - LETTER_WIDTH ) /2 )
HOST = "192.168.1.20"
PORT = 8888
def stop():
    global running
    running=0


def getSymbol():
    global sMessage, msocket,ballDone, iStep,HOST, PORT, apo
    try:
       
         msocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
         msocket.connect((HOST,PORT))
         msocket.sendall("GET /?pos=1\r\n\r\n")
         str = ""
         data = msocket.recv(2)
         print "Got -"+data+"-" 
         if data:
            str += data
            if sMessage != str.upper():
                sMessage = str.upper()
                ballDone = False
                iStep = 0
         msocket.close()  
         e32.ao_sleep(1)         
    except:
        sMessage = "="



def callback(event):
    global  iStep, sMessage,ballDone
    if event['type'] == appuifw.EEventKey:
       charCode=event['scancode']
       if ( charCode > 64 and iCharCode < 91):
            sMessage=chr(charCode)            
       else:
            print charCode
       ballDone = False
       iStep = 0
      

def drawLetter(iSpriteRow, iSpriteCol):  
    global iStep, LETTER_HEIGHT, LETTER_WIDTH, canvas,  ballDone, X, scale, HEIGHT 
    yPos = (HEIGHT ) - iStep;
   
    if ((yPos > 30 ) ):
        canvas.clear(0x000000)
        canvas.blit(img, source=[(iSpriteCol * LETTER_WIDTH, iSpriteRow * LETTER_HEIGHT),((iSpriteCol +1 ) * LETTER_WIDTH, (iSpriteRow +1) * LETTER_HEIGHT)],
         target=( X, yPos), scale=scale)
        ballDone = False
    else:
        ballDone = True 

def handle_redraw(rect):
  global running, iStep,  ballDone
  
  iCounter = 0
  iCharCode = 0
    
  for iCounter in range(0, len(sMessage.upper())):
    iCharCode = ord(sMessage[iCounter])  
    if (iCharCode > 64 and iCharCode < 91):
        iSpriteCol = (iCharCode - 65 ) % 10
        iSpriteRow = math.floor((iCharCode - 65) / 10)
        letter = chr(iCharCode)
    elif (iCharCode > 47 and iCharCode < 58):
        iSpriteCol = (iCharCode - 48 ) 
        iSpriteRow = 5
        letter = chr(iCharCode)    
    else:
        iSpriteCol = 6
        iSpriteRow = 2
        letter = " " 
    drawLetter(iSpriteRow, iSpriteCol)
    #print ballDone, letter, iSpriteRow, iSpriteCol
  if not ballDone:
    iStep += 5
  e32.reset_inactivity()


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

AP='c:\\data\\python\ap.txt'    
apo=None 
getAccessPoint() 
apo.start()
running=1
iCharCode=0
# define the canvas, include the redraw callback function
canvas=appuifw.Canvas(event_callback=callback,redraw_callback=handle_redraw)
# set the app.body to canvas
appuifw.app.body=canvas
canvas.clear(0x000000)
app.exit_key_handler=quit
canvas.bind(EKeyDownArrow,stop)
getSymbol()
ballDone=False      
# create a loop to redraw the the screen again and again until the exit button is pressed
while running:
    if ballDone:
       getSymbol()
    # redraw the screen
    handle_redraw(())
    # yield needs to be here in order that key pressings can be noticed
    e32.ao_sleep(0.09)
apo.stop()    
print "-------------------"
