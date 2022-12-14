#Basic Colored Text Animation with stdout in Python
#Author : OpniXGH - FA2AS Facebook Group

import sys,time
t=0.05
welcome="Welcome to Basic Animation in Python!\n"
def equals():
  for i in range(32):
    #merubah warna text dengan warna merah
    x="\033[1;31m"
    sys.stdout.write(x+"=");
    time.sleep(t)
    #memflush layar agar text dapat dicetak satu persatu
    sys.stdout.flush()
equals()
print "\n"
for i in welcome:
  #merubah warna text dengan warna cyan
  x="\033[1;36m"
  sys.stdout.write(x+i)
  time.sleep(t)
  sys.stdout.flush()
#merubah kembali warna text ke warna asal
print "\033[0m"
equals()
print "\033[0m"
print
