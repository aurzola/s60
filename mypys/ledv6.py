#
# Screen is 240x320 pixels
# 
import appuifw
from appuifw import *
from key_codes import *
import e32, graphics, math
import sys
from graphics import *
import sysinfo
import urllib

try:
    sys.modules['socket'] = __import__('btsocket')
except ImportError:
    pass
import socket

def downloadImg(iCharCode):
    global HOST,PORT
    pathImg="c:\\data\\images\\"+str(iCharCode)+".jpg"
    try: 
        x = Image.open(pathImg)
        #print "existe"
    except Exception,e: 
        URL="http://"+HOST+":"+str(PORT)+"/img/"+str(iCharCode)
        urllib.urlretrieve(URL, pathImg)
    
def downloadImgs():
    for x in range(65, 91):
        downloadImg(x)
    for x in range(48, 58):
        downloadImg(x)

# create an exit handler
def quit():
    global running
    running=0
    appuifw.app.set_exit()

# set the screen size to large
appuifw.app.screen='full'
print "imei " + sysinfo.imei()
# define an initial image (white)
BLANKIMG = Image.new((2,2))
img = BLANKIMG
sMessage = "2"
scale = 0
LETTER_HEIGHT = 250  #152 
LETTER_WIDTH = 160 #100
HEIGHT = 240
iStep = 0 
X= math.floor( (320 - LETTER_WIDTH ) /2 )
HOST = "192.168.1.10"
PORT = 8888
def stop():
    global running
    running=0


def getSymbol():
    global sMessage, msocket,ballDone, iStep,HOST, PORT, apo
    try:
         msocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
         msocket.connect((HOST,PORT))
         msocket.sendall("GET /i?imei="+sysinfo.imei()+"\r\n\r\n")
         str = ""
         data = msocket.recv(2)
        # print "Got -"+data+"-" 
         if data:
            str += data
            if sMessage != str.upper():
                sMessage = str.upper()
                ballDone = False
                loadImg()
                iStep = 0
            else:
                e32.ao_sleep(5)
         else:
            sMessage= " "        
         msocket.close()  
         #e32.ao_sleep(1)         
    except:
        sMessage = " "

def loadImg():
    global img
    iCharCode = ord(sMessage[0])  
   
    if (iCharCode > 64 and iCharCode < 91):
        img = Image.open("c:\\data\\images\\"+str(iCharCode)+".jpg")
        letter = chr(iCharCode)
    elif (iCharCode > 47 and iCharCode < 58):
        img = Image.open(u"c:\\data\\images\\"+str(iCharCode)+".jpg")
        letter = chr(iCharCode)    
    else:
        #img = Image.open(u"c:\\data\\images\\noimage.jpg")
	img = BLANKIMG
        letter = " " 



def callback(event):
    global  iStep, sMessage,ballDone
    if event['type'] == appuifw.EEventKey:
       charCode=event['scancode']
       if ( charCode > 64 and iCharCode < 91):
            sMessage=chr(charCode)
            loadImg()
       else:
            print charCode
       ballDone = False
       iStep = 0
      

def drawLetter():  
    global iStep, canvas,  ballDone, X, scale, HEIGHT, img 
    yPos = (HEIGHT ) - iStep;
   
    if ((yPos > 20 ) ):
        canvas.clear(0x000000)
        canvas.blit(img, target=( X, yPos), scale=scale)
        ballDone = False
    else:
        ballDone = True 

def handle_redraw(rect):
  global running, iStep,  ballDone
  
  iCounter = 0
  iCharCode = 0
  drawLetter()
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

AP='c:\\data\\python\ap3.txt'    
apo=None 
getAccessPoint() 
apo.start()
downloadImgs()
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
