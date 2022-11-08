import sys
import audio, appuifw
try:
    sys.modules['socket'] = __import__('btsocket')
except ImportError:
    pass
 
import socket
from appuifw import note, popup_menu

#Define the function for stopping the playback
def stop():
    global m
    m.stop()
    m.close()

appuifw.app.exit_key_handler=stop
 
#Open the sound file
m=audio.Sound.open("C:\\Data\\Sounds\\er.mp3")

ap_id = socket.select_access_point()
apo = socket.access_point(ap_id)
socket.set_default_access_point(apo)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('0.0.0.0',4321))
s.listen(1)
while True:
    sock,addr = s.accept()
    fsock = sock.makefile()
    print "New connection from",addr
    while True:
        line = fsock.readline()
        if not line:
            print "Connection closed"
            break
	if line.startswith('quit'):
	    s.close()
	    apo.stop()
        sys.exit()
	if line.startswith('play'):
	    m.play()
	audio.say(line)
        print ">> ",line
