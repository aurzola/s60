import sys
import e32, os
import audio, appuifw
try:
    sys.modules['socket'] = __import__('btsocket')
except ImportError:
    pass
 
import socket
from appuifw import note, popup_menu


PORT=12345
AP='c:\\data\\python\ap.txt'

def set_accesspoint():
    apid = socket.select_access_point()
    if appuifw.query(u"Set as default access point","query") == True:
        f = open(AP,'w')
        f.write(repr(apid))
        f.close()
        appuifw.note(u"Saved default access point ", "info")
        apo = socket.access_point(apid)
        socket.set_default_access_point(apo)

        
def stop():
    global running
    running = 0

def getAccessPoint():
    global apo
    try:
        f=open(AP,'rb')
        setting = f.read()
        apid = eval(setting)
        f.close()
        if not apid == None :
            apo = socket.access_point(apid)
            socket.set_default_access_point(apo)
        else:
            set_accesspoint()
    except:
        set_accesspoint()

        

running = 1
appuifw.app.menu = [(u"stop", stop)]
appuifw.app.exit_key_handler=stop
apo = None
file = u'c:\\data\\download\\ledtext.txt'
#ap_id = socket.select_access_point()
#apo = socket.access_point(ap_id)
#socket.set_default_access_point(apo)

getAccessPoint()

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ( "%s : %i" % ( apo.ip() , PORT) )
s.bind(('0.0.0.0',PORT))
s.listen(1)
while running:
    print "ledText Accepting conxs"
    sock,addr = s.accept()
    sock.setblocking(0)
    fsock = sock.makefile()
    print "New connection from",addr
    while running:
        line = fsock.readline()
        if not line:
            sock.close()
            print "Connection closed"
            break
        e32.ao_yield()    
        if line.startswith('quit'):
                fsock.close()
                sock.close()
                s.close()
                apo.stop()
                sys.exit()
        else:
                f = open(file,'w')
                f.write(u'   '+line.upper())
                f.close()
                print "Get text: " + line
                #appuifw.note(u"Saved text", "info")
        
print "Server stopped"        
