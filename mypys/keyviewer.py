#
# keyviewer.py
#
# Copyright (c) 2005 Nokia. All rights reserved.
#

import appuifw
import graphics
import e32

keyboard_state={}
last_keycode=0

def draw_state():
    canvas.clear()
    canvas.text((0,12),u'Scancodes of pressed keys:',0x008000)
    canvas.text((0,24),u' '.join([unicode(k) for k in keyboard_state if keyboard_state[k]]))
    canvas.text((0,36),u' '.join([unicode(hex(k)) for k in keyboard_state if keyboard_state[k]]))
    canvas.text((0,48),u'Last received keycode:', 0x008000)    
    canvas.text((0,60),u'%s (0x%x)'%(last_keycode,last_keycode))
    canvas.text((0,80),u'char = %s '%(chr(last_keycode)))
    
def callback(event):
    global last_keycode
    if event['type'] == appuifw.EEventKeyDown:
        keyboard_state[event['scancode']]=1
    elif event['type'] == appuifw.EEventKeyUp:
        keyboard_state[event['scancode']]=0
    elif event['type'] == appuifw.EEventKey:
        last_keycode=event['keycode']
    draw_state()

canvas=appuifw.Canvas(event_callback=callback,
                      redraw_callback=lambda rect:draw_state())
appuifw.app.body=canvas

lock=e32.Ao_lock()
appuifw.app.exit_key_handler=lock.signal
lock.wait()
