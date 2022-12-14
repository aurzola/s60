import e32

import pys60usb

while 1:
    try:
        conn = pys60usb.USBConnection()
        conn.connect()
        print "connected.."
        while 1:
            print conn.recv(1)
    except:
        print "got error"
