import sys
import e32, os
import audio, appuifw
try:
    sys.modules['socket'] = __import__('btsocket')
except ImportError:
    pass
 
import socket
from appuifw import note, popup_menu


PORT=4321
AP='c:\\data\\python\ap.txt'

def set_accesspoint():
    apid = socket.select_access_point()
    if appuifw.query(u"Set as default access point","query") == True:
        f = open(AP,'w')
        f.write(repr(apid))
        f.close()
        appuifw.note(u"Saved default access point ", "info")
        apo = socket.access_point(apid)
        socket.set_default_access_point(apo)

#Define the function for  the playback
def playCallback(prevState, currState, err):
    global idxPlay, arrSong 
    if ( prevState == 2 and currState == 1 ):
        idxPlay = ( idxPlay + 1 ) %  len(arrSong)
        startPlay(idxPlay)
        
def setVol(vol):
    global M
    M.set_volume(vol % M.max_volume())

def startPlay(idx):
    global M, arrSong, vol
    try:
        stopPlay()
        fileName = "e:\\download\\" + arrSong[idx % len(arrSong)]
        print "Playing " + fileName
        M = audio.Sound.open(fileName)
        M.play(callback=playCallback)
        setVol(vol)
    except:
        print "File not found"

def stopPlay():
    try:
        global M
        M.stop()
        M.close()
    except:
        print "not playing"
        
def stop():
    global running
    running = 0

def listMp3():
    global arrSong
    p = os.listdir('e:\\download\\')
    j = 0
    for i in range(len(p)):
        if ( p[i].endswith("mp3") ):
            arrSong.append(u""+p[i])
            j = j + 1

def getAccessPoint():
    global apo
    try:
        f=open(AP,'rb')
        setting = f.read()
        apid = eval(setting)
        f.close()
        if not apid == None :
            apo = socket.access_point(apid)
            socket.set_default_access_point(apo)
        else:
            set_accesspoint()
    except:
        set_accesspoint()

def sendPList(fsock):
    global arrSong, idxPlay, vol
    fsock.write("Volume " +str(vol) + '\n')
    for index in range(len(arrSong)):
        fsock.write( str(index) + ".- " + arrSong[index] )
        if ( index == idxPlay ):
            fsock.write('  <----- ' )    
        fsock.write('\n' )
    fsock.flush()    
        
vol = 6        
M = 0
running = 1
appuifw.app.menu = [(u"stop", stop)]
appuifw.app.exit_key_handler=stop
arrSong = []
idxPlay = 0
apo = None
#ap_id = socket.select_access_point()
#apo = socket.access_point(ap_id)
#socket.set_default_access_point(apo)

getAccessPoint()

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listMp3()
print ( "%s : %i" % ( apo.ip() , PORT) )
s.bind(('0.0.0.0',PORT))
s.listen(3)
while running:
    print "Accepting conxs"
    sock,addr = s.accept()
    sock.setblocking(0)
    fsock = sock.makefile()
    print "New connection from",addr
    sendPList(fsock)
    while running:
        line = fsock.readline()
        #line = fsock.recv(128)
        if not line:
            sock.close()
            print "Connection closed"
            break
        e32.ao_yield()    
        print ">> ", line            
        if line.startswith('stop'):
            stopPlay()
        elif line.startswith('bye'):
            sock.close()
            break
        elif line.startswith('mute'):
            vol=0
            setVol(vol)
        elif line.startswith('-'):
            vol = vol - 2
            if ( vol < 0 ):
                vol = 0
            setVol(vol)    
        elif line.startswith('+'):
            vol = vol + 2
            setVol(vol)   
        elif line.startswith('ls'):
            sendPList(fsock)
        elif line.startswith('play'):
            startPlay(idxPlay)
        elif line.startswith('>'):
            idxPlay += 1 
            idxPlay = idxPlay % len(arrSong)
            startPlay(idxPlay)    
        elif line.startswith('<'):
            idxPlay -= 1
            if ( idxPlay == 0 ):
                idxPlay = len(arrSong)
            startPlay(idxPlay)    
        else:
            if line.startswith('quit'):
                stopPlay()
                sock.close()
                s.close()
                apo.stop()
                sys.exit()
            else:
                try:
                   idxPlay = int(line)
                   startPlay(idxPlay)
                except ValueError:
                    print("That's not an idx song!")
        
print "Server stopped"        
