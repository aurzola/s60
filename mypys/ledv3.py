import appuifw
from appuifw import *
from key_codes import *
import e32, graphics, math

# create an exit handler
def quit():
    global running
    running=0
    appuifw.app.set_exit()

# set the screen size to large
appuifw.app.screen='full'

# define an initial image (white)
img=graphics.Image.open(u'c:\\data\\images\\redledfont-002.jpg')
sMessage = "   FELIZ NAVIDAD - FELIZ 2023"
LETTER_HEIGHT = 144.5 
LETTER_WIDTH = 116.5 # casi
iStep = 0 
iDrawPhase = 0
ballDone = True

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
    #sMessage = "   FELIZ 2008"
def stop():
    global running
    running=0


def callback(event):
    global iCharCode
    if event['type'] == appuifw.EEventKey:
	iCharCode=event['scancode']


def drawLetter(iSpriteRow, iSpriteCol,  iPos, letter):  
    global iStep, LETTER_HEIGHT, LETTER_WIDTH, canvas,  ballDone 
    xPos = (LETTER_WIDTH * iPos) - iStep;
    xPos = math.floor (xPos)
    if ((xPos > 0 - LETTER_WIDTH) and (xPos < 319 + LETTER_WIDTH)):
        canvas.blit(img, source=[(iSpriteCol * LETTER_WIDTH, iSpriteRow * LETTER_HEIGHT),((iSpriteCol +1 ) * LETTER_WIDTH  , (iSpriteRow +1) * LETTER_HEIGHT)]  , target=(xPos, 0))
        ballDone = False


def handle_redraw(rect):
  global running, iStep,  ballDone
  
  iCounter = 0
  iCharCode = 0
  ballDone = True
  for iCounter in range(0, len(sMessage)):
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
    drawLetter(iSpriteRow, iSpriteCol, iCounter, letter)
    #print iCharCode,iSpriteRow, iSpriteCol
  if (ballDone):
#    getText()
    iStep = 0
  else:
    iStep += 20
  e32.reset_inactivity()
      
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
    e32.ao_sleep(0.08)
print "-------------------"
