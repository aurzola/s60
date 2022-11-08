# Sound recording / playing script 

import appuifw, e32, audio


filename = 'e:\\download\\silent-night-disco.mp3'


def playing():
    global S
    try:
        S=audio.Sound.open(filename)
        S.play()
        print "Playing"
    except:
        print "File not found"

def closing():
    global S
    S.stop()
    S.close()
    print "Stopped"

def quit():
    script_lock.signal()
    appuifw.app.set_exit()

appuifw.app.menu = [(u"play", playing),
                    (u"stop", closing)]

appuifw.app.title = u"Sound recorder"

appuifw.app.exit_key_handler = quit
script_lock = e32.Ao_lock()
script_lock.wait()


 