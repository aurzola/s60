import sys
import appuifw
try:
    sys.modules['socket'] = __import__('btsocket')
except ImportError:
    pass
 
import socket
from appuifw import note, popup_menu

HOST = '192.168.1.101'    # The remote host
PORT = 8765              # The same port as used by the server

ap_id = socket.select_access_point()
apo = socket.access_point(ap_id)
socket.set_default_access_point(apo)
print "define socket"
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


print "Tratando de Conectarse"
s.connect((HOST, PORT))
print "connected"
s.sendall('SEND_ONCE CABLE ch+\n\r')
s.sendall('SEND_ONCE CABLE epg\n\r')
print "data send"
data = s.recv(1024)
s.close()
print 'Received', `data`
