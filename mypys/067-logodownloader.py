import sys
import appuifw
import e32
from graphics import *
try:
    sys.modules['socket'] = __import__('btsocket')
except ImportError:
    pass

import urllib
 
import socket
#access point is selected from the list
apid = socket.select_access_point()
apo = socket.access_point(apid)
apo.start()
dest_file = u"c:\\data\\images\\python-logo.gif"
URL = "http://comercializa.com.co/img/logo.png"
lock = e32.Ao_lock()
try: 
    x = Image.open(dest_file)
    print "existe"
except Exception,e: 
    print str(e)
    urllib.urlretrieve(URL, dest_file)
    viewer = appuifw.Content_handler(lock.signal)
    viewer.open(dest_file)
    lock.wait()     
apo.stop()

print "end"
