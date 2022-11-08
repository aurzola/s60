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
img=graphics.Image.open(u'c:\\data\\download\\redledfont.jpg')
LETTER_HEIGHT = 144.5 
LETTER_WIDTH = 116.5 # casi
iStep = 0 
iDrawPhase = 0
ballDone = True

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
    global running, iStep,  ballDone, iCharCode
    
    if (iCharCode > 64 and iCharCode < 91):
        iSpriteCol = (iCharCode - 65 ) % 10
        iSpriteRow = math.floor((iCharCode - 65) / 10)
        letter = chr(iCharCode)
    else:
        iSpriteCol = 6
        iSpriteRow = 2
        letter = " " 
    drawLetter(iSpriteRow, iSpriteCol, 0, letter)
    #print iCharCode,iSpriteRow, iSpriteCol

running=1
iCharCode=0
# define the canvas, include the redraw callback function
canvas=appuifw.Canvas(event_callback=callback,redraw_callback=handle_redraw)

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
print "-------------------"
