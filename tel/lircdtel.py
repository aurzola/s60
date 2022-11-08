try:
    from btsocket import *
except:
    from socket import *

HOST = '192.168.1.101'    # The remote host
PORT = 8765              # The same port as used by the server
print "define socket"
s = socket.socket(AF_INET, SOCK_STREAM)
print "trying to connect to socket"
s.connect((HOST, PORT))
print "connected"
s.send('SEND_ONCE CABLE ch+')
print "data send"
data = s.recv(1024)
s.close()
print 'Received', `data`
