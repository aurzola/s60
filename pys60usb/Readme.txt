pys60usb - usb connectivity for s60/python

With this you can communicate between phone and pc via the usb cable
(Nokia DKU-2).

Included is an example USB version of the familiar "BT Console".

Required software:
- windows: Nokia PC Suite (tested with 6.6.18)
or
- linux: cdc_acm module
  
Setup instructions
==================

Windows:
- enable USB connectivity on the PC Suite
- when you plugin the phone cable, Control Panel->Phone and Modem Options
  'Modems' tab should have "Nokia XXXX USB modem", connected to some 
  virtual serial port. You can test the connection by starting hyperterminal,
  and typing "AT<enter>". The phone's Fax/Modem process should reply with "OK".
- Leave HyperTerminal open

Note: it might be possible to use usbser.sys on Windows to get serial
port support for the usb device. See the included gadget_serial.txt
for more info. I failed to get that working.


Linux:
(this info is from Fatal @ freenode #pys60)
- setup cdc_acm module
- connect minicom/picocom/etc to /dev/ttyACMx

Note: kernel oops if you disconnect when terminal is accessing
/dev/ttyACMx. This problem is notified to maintainer.

Phone setup:
- Copy the file symbian\bin\armi\urel to phone system\libs
- Kill FaxModem process (this *might* not be required in all
  phones). Note, that in some phones you might need to do this many
  times.
- copy python\phone\simpleusbconsole.py to phone and run it
- now you should see python prompt in the HyperTerminal


author: ssalmine@users.sf.net / ranq @ freenode #pys60

Known issues:
Throws Kern-Exec 3 when stopping the simpleusbconsole.py.
Sometimes the serial port stops responding. Re-attach the cable.

CHANGELOG:
v0.20070610:
 .: Modified by jtoivola
  * Added parameters for connect() -method
  * Changed default accessmode to ECommShared. No need to kill FaxModem at least on N70.    
  * Fixed: Raises exceptions too often.
    
v0.20060101:  
 .: bug fix release
  * added setup instructions for linux
  * fax/modem killing should work now (see test_killfaxmodem.py)

v0.20051028:
 .: initial version - alpha quality
 
