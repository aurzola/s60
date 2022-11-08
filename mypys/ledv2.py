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
appuifw.app.screen='large'

# define an initial image (white)
img=graphics.Image.open(u'c:\\data\\images\\blueled.jpg')

sMessage = "   FELIZ NAVIDAD"
LETTER_HEIGHT = 220 
LETTER_WIDTH = 182.84 # casi
iStep = 0 
iDrawPhase = 0
ballDone = True

def stop():
    global running
    running=0

def event(ev):
    """Event handler"""
    pass

def getText():
    global sMessage, fileText
    try:
        f=open(fileText,'r')
        sMessage = f.read()
        print "getText " + sMessage
        f.close()
    except:
        f=open(fileText,'w')
        f.write(sMessage)
        f.close()

def drawLetter(iSpriteRow, iSpriteCol,  iPos, letter):
  global iStep, LETTER_HEIGHT, LETTER_WIDTH, canvas,  ballDone 
  xPos = (LETTER_WIDTH * iPos) - iStep;
  xPos = math.floor (xPos)
  if ((xPos > 0 - LETTER_WIDTH) and (xPos < 319 + LETTER_WIDTH)):
    canvas.blit(img, source=[(iSpriteCol * LETTER_WIDTH, iSpriteRow),((iSpriteCol +1 ) * LETTER_WIDTH  , iSpriteRow + LETTER_HEIGHT)]  , target=(xPos, 0))
    ballDone = False
    #print ("%f - %s " %  (xPos , letter))
  #print "-----"
# define your redraw function (that redraws the picture on and on)
# in this case we redraw the image named img using the blit function
def handle_redraw(rect):
  global running, iStep,  ballDone
  iCounter = 0
  iCharCode = 0
  ballDone = True
  for iCounter in range(0, len(sMessage)):
    iCharCode = ord(sMessage[iCounter])
    if (iCharCode > 64 and iCharCode < 91):
      iSpriteCol = ( iCharCode - 65) 
      iSpriteRow = 0
    else:
      iSpriteCol = 26
      iSpriteRow = 0  
    #print iSpriteRow, iSpriteCol
    
    drawLetter(iSpriteRow, iSpriteCol, iCounter, sMessage[iCounter])
    
  if (ballDone):
    getText()
    iStep = 0
  else:
    iStep += 20
  e32.reset_inactivity()
  
running=1
fileText = u'c:\\data\\download\\ledtext.txt'
getText()
# define the canvas, include the redraw callback function
canvas=appuifw.Canvas(redraw_callback=handle_redraw)

# set the app.body to canvas
appuifw.app.body=canvas

app.exit_key_handler=quit
canvas.bind(EKeyDownArrow,stop)
# create a loop to redraw the the screen again and again until the exit button is pressed
while running:
    # redraw the screen
    handle_redraw(())
    # yield needs to be here in order that key pressings can be noticed
    #e32.ao_yield()  #WAS aur test 
    e32.ao_sleep(0.1)
print sMessage    
print "-------------------"

