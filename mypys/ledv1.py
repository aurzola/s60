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
img=graphics.Image.open(u'c:\\data\\images\\redled.jpg')

sMessage = "  MERRY CHRISTMAS  "
LETTER_HEIGHT = 136 
LETTER_WIDTH = 116
iStep = 0 
iDrawPhase = 0

#img.rectangle((0,0,160,219),0x00ff00)
img2= graphics.Image.new((48,48));
def stop():
	global running
	running=0

def event(ev):
    """Event handler"""
    pass

def drawLetter(iSpriteRow, iSpriteCol,  iPos):
	global iStep, LETTER_HEIGHT, LETTER_WIDTH, canvas
	xPos = (LETTER_WIDTH * iPos) - iStep;
	
	if ((xPos > 0 - LETTER_WIDTH) and (xPos < 319 + LETTER_WIDTH)):
		#canvas.blit(img, (iSpriteCol * LETTER_WIDTH, iSpriteRow * LETTER_HEIGHT, iSpriteCol * LETTER_WIDTH+ LETTER_WIDTH, iSpriteRow * LETTER_HEIGHT +LETTER_HEIGHT ) , (xPos, 0))
		#canvas.blit(img, (iSpriteCol * LETTER_WIDTH, iSpriteRow * LETTER_HEIGHT) , (xPos, 0))
		#canvas.blit(img, source=(iSpriteCol * LETTER_WIDTH, iSpriteRow * LETTER_HEIGHT) , target=(xPos, 50))
		#source=((0,0),(None,None))
		#canvas.blit(img, source=((232, 0), (50,50)),  target=(0, 0))
		canvas.blit(img, source=(232, 0),  target=(0, 0))
		#print img.size

# define your redraw function (that redraws the picture on and on)
# in this case we redraw the image named img using the blit function
def handle_redraw(rect):
	global running, iStep
	iCounter = 0
	iCharCode = 0
	for iCounter in range(0, len(sMessage)):
		iCharCode = ord(sMessage[iCounter])
		if (iCharCode > 64 and iCharCode < 91):
			iSpriteCol = ( iCharCode - 65) % 10 
			iSpriteRow = math.floor(( iCharCode - 65) / 3);
		else:
			iSpriteCol = 6
			iSpriteRow = 2	
		#print iSpriteRow, iSpriteCol
		drawLetter(iSpriteRow, iSpriteCol, iCounter)
	iStep += 20;
	e32.reset_inactivity()
	
running=1

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
#print "-------------------"

