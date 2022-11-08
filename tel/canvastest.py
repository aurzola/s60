import appuifw, e32, graphics, sysinfo
from key_codes import *
app_lock = e32.Ao_lock()
#Define the exit function
def quit():
  app_lock.signal()
appuifw.app.exit_key_handler = quit
 
#Set the screen to full
appuifw.app.screen = 'full'
 
#Get the screen's width and height
screen_w, screen_h = sysinfo.display_pixels()
 
#Define a set of coordinates at which a dot will be drawn on the image
coord = (screen_w / 2, screen_h / 2)
 
#Define a function that will be called when the canvas needs to be redrawn
def handle_redraw(rect):
  #Clear the canvas
  c.clear()
  #Write text
  c.text((screen_w / 10, screen_h - screen_h / 10), u"Move the dot", 0x008000, font=(u'Nokia Hindi S60', 35, appuifw.STYLE_BOLD))
  #Draw the dot
  c.point(coord, 0xff0000, width=10)
 
#Define a function that will be called when one of the bound keys is pressed
def move(direction):
  global coord
  #Modify the dot's coordinates by 10 pixels according to the direction
  if (direction == 'left') and (coord[0] - 10 >= 0):
     coord = (coord[0] - 10, coord[1])
  if (direction == 'right') and (coord[0] + 10 <= screen_w):
     coord = (coord[0] + 10, coord[1])
  if (direction == 'up') and (coord[1] - 10 >= 0):
     coord = (coord[0], coord[1] - 10)
  if (direction == 'down') and (coord[1] + 10 <= screen_h):
     coord = (coord[0], coord[1] + 10)
  #Redraw the canvas
  handle_redraw(())
 
#Create an instance of Canvas and set it as the application's body
c = appuifw.Canvas(redraw_callback=handle_redraw)
appuifw.app.body = c
 
#Bind the navigation keys
c.bind(EKeyLeftArrow, lambda:move('left'))
c.bind(EKeyRightArrow, lambda:move('right'))
c.bind(EKeyUpArrow, lambda:move('up'))
c.bind(EKeyDownArrow, lambda:move('down'))
 
#Wait for the user to request the exit
app_lock.wait()
