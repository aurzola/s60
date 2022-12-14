# WARNING
# killing faxmodem causes some system instability, at least in my 7610.
# for example, it might close down bluetooth


# XXXX this does not actually work yet

import pys60usb

print "killing faxmodem"
pys60usb.kill_faxmodem()
print "done"
