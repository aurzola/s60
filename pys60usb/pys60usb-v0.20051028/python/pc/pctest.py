"""
usage:
 pctest.py <comport>

 <comport> : COM1, COM2 etc..
"""
import sys
import time

# run this in pc side
# requires pyserial-extension
import serial


def main():
    if len(sys.argv) < 2:
        print __doc__
        return

    port = int(sys.argv[1][-1]) - 1
    print "opening port", port + 1
    ser = serial.Serial(port)
    print "opened", ser.portstr

    start = time.time()
    bytes = 0
    while 1:
        inp = ser.read(1024) # read max len(out)
        bytes += len(inp)
        if len(inp) == 0:
            break
        print "read <-", len(inp), inp

    end = time.time()

    print "KiB/s", (bytes / 1024.) / (end-start)

if __name__ == "__main__":
    main()

