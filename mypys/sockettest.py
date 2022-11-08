import sys
import appuifw
try:
    sys.modules['socket'] = __import__('btsocket')
except ImportError:
    pass
 
import socket
#access point is selected from the list
apid = socket.select_access_point()
apo = socket.access_point(apid)
socket.set_default_access_point(apo)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print apo.ip()
s.connect(('comercializa.com.co',80))
s.send('GET /\r\n\r\n')
data = s.recv(1024)
s.close()
apo.stop()
print 'Received', `data`
