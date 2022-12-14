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

sock=pys60usb.USBConnection() 

print "Connecting to PC via USB"
sock.connect()
socketio=socket_stdio(sock)
realio=(sys.stdout,sys.stdin,sys.stderr)
(sys.stdout,sys.stdin,sys.stderr)=(socketio,socketio,socketio)
import code
try:
  code.interact()
finally:
  (sys.stdout,sys.stdin,sys.stderr)=realio
  sock.close()
