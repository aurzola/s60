"""
pys60usb - usb connectivity on s60/python

class USBConnection()
 connect()
 send(data, timeout)
 data = recv(bytecount, timeout)
 close()
"""
import e32

import pys60usb

conn = pys60usb.USBConnection()
conn.connect()

print "connected.."
blob = 'abc'*1000
try:
    for i in range(1000):
        conn.send(blob)
finally:    
    conn.close()
