'''
Access Point Test

Copyright (c) 2009 Jouni Miettunen
http://jouni.miettunen.googlepages.com/

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

1.00 2009-03-19 Initial release
     Based on Forum Nokia wiki samples
     Based on experiments done with not-yet-released app

Coding music by Parov Stelar:
- Libella Swing
- Flame of Fame
'''

import e32
import appuifw

# Warning: it takes a long time to import these two!
import socket
import urllib

VERSION = u"1.00"

# Global variables
g_apid = 0
g_text = None

def show_text(a_text=""):
    ''' Put some text on-screen '''
    g_text.clear()
    if a_text:
        g_text.add(unicode(a_text))
    else:
        g_text.add(u"Testing (default) Access Point." +\
            u"Check Options menu for operations.\n\n" +\
            u"Enjoy,\n\n--jouni")

def select_ap(a_id=0):
    ''' Select temporary default access point '''
    if a_id:
        apid = a_id
    else:
        apid = socket.select_access_point()

    # zero is not a valid AP number
    if apid:
        apo = socket.access_point(apid)
        socket.set_default_access_point(apo)
        return apo
    else:
        return None

def menu_fetch_url(a_url="", a_ap=0):
    ''' Fetch given URL using given access point '''
    # Tell user something is happening
    show_text("Trying to fetch:\n\n" + a_url)
    # Show user something is happening
    e32.ao_yield()

    # Set access point
    # Note that id is used only to find access point
    apo = select_ap(a_ap)
    if not apo:
        appuifw.note(u"Cancelled!")
        show_text()
        return

    if a_url:
        f = urllib.urlopen(a_url)
        d = f.read()
        f.close()
        apo.stop()
        show_text(d)
    else:
        appuifw.note(u"Missing URL!")

def menu_default_ap():
    ''' Ask user to select default access point '''
    global g_apid
    g_apid = socket.select_access_point()

def menu_clear_ap():
    ''' Forget default access point selection '''
    global g_apid
    g_apid = 0

def menu_about():
    ''' Callback for menu item About '''
    appuifw.note(u'Access Point Test v'+VERSION+'\n'+\
        u'jouni.miettunen.googlepages.com\n\u00a92009 Jouni Miettunen')

def cb_quit():
    ''' Clean-up before application exit '''
    app_lock.signal()

# Initialize application
appuifw.app.orientation = 'portrait'
appuifw.app.title = u'Test AP'
appuifw.app.exit_key_handler = cb_quit
appuifw.app.menu = [
    (u"Fetch google.com", lambda:menu_fetch_url("http://www.google.com/webhp", g_apid)),
    (u"Access point", (
        (u"Set default AP", menu_default_ap),
        (u"Clear default AP", menu_clear_ap))),
    (u"About", menu_about),
    (u"Exit", cb_quit)]

# Initialize application UI
g_text = appuifw.Text()
appuifw.app.body = g_text
show_text()

# Wait for user to do anything
app_lock = e32.Ao_lock()
app_lock.wait()
