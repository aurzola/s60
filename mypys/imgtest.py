#Copyright (c) 2008 Pankaj Nathani
#Opening an image or creating a blank one

import graphics, e32, appuifw


#Define the exit function
def quit():
    app_lock.signal()
appuifw.app.exit_key_handler=quit

canvas=appuifw.Canvas()
appuifw.app.body=canvas

#We open an existing picture

#pic=graphics.Image.open(u'c:\\data\\download\\tnt.jpg')
pic=graphics.Image.open(u'c:\\data\\images\\letters-pink.jpg')
#And also make a blank one
img=graphics.Image.new((48,48)) #Remember to specify the appropriate size in pixels

#canvas.blit(pic)
canvas.blit(pic, target=(0,0))
#Sets the background as the picture

#Wait 5 seconds
#e32.ao_sleep(5)

#canvas.blit(img, target=(70,70))
#Sets the background to the blank image

app_lock=e32.Ao_lock()
app_lock.wait()
 
