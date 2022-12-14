# Copyright (c) 2004 Nokia
# Programming example -- see license agreement for additional rights
# A simple interactive console over Bluetooth.

import pys60usb

class socket_stdio:
    def __init__(self,sock):
        self.socket=sock
    def read(self,n=1):
        return self.socket.recv(n)
    def write(self,str):
        return self.socket.send(str.replace('\n','\r\n'))
    def readline(self,n=None):
        buffer=[]
        while 1:
            ch=self.read(1)
            if ch == '\n' or ch == '\r':   # return
                buffer.append('\n')
                self.write('\n')
                break
            if ch == '\177' or ch == '\010': # backspace
                self.write('\010 \010') # erase character from the screen
                del buffer[-1:] # and from the buffer
            else:
                self.write(ch)
                buffer.append(ch)
            if n and len(buffer)>=n:
                break
        return ''.join(buffer)
    def raw_input(self,prompt=""):
        self.write(prompt)
        return self.readline()
    def flush(self):
        pass

sock = pys60usb.USBConnection()
modes     = [ "ECommExclusive", "ECommShared", "ECommPreemptable"]
roles     = [ "ECommRoleDCE",   "ECommRoleDTE" ]
porttypes = [ u"ACM"]
ports     = 5

for porttype in porttypes:
    print
    print porttype,
    connected = False
    
    for role in roles:
        print role,
        role = getattr( pys60usb, role )
        for mode in modes:
            print mode,
            mode = getattr( pys60usb, mode )
            
            for port in xrange( ports ):
                print port,

                try:
                    sock.connect( port, porttype, mode, role )
                except Exception, msg:
                    #print msg
                    continue
                
                print 
                print "Successfully connected"
                
                socketio=socket_stdio(sock)
                realio=(sys.stdout,sys.stdin,sys.stderr)
                (sys.stdout,sys.stdin,sys.stderr)=(socketio,socketio,socketio)
                
                import code
                try:
                  code.interact()
                finally:
                  (sys.stdout,sys.stdin,sys.stderr)=realio
                  sock.close()
                connected = True

            if connected: break
        if connected: break
    if connected: break

