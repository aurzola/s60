# WARNING

# killing faxmodem might cause some system instability, at least in my
# 7610 that happens.  for example, it might close down bluetooth.

import pys60usb

print "trying to kill faxmodem"
pys60usb.kill_faxmodem()
print "done"
