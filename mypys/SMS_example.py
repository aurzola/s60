# Copyright (c) 2004 Nokia
# Programming example -- see license agreement for additional rights
# SMS sending example application

import appuifw
import e32
# import messaging 
import sysinfo

old_title = appuifw.app.title
appuifw.app.title = u"SMS sending"



class ChoiceView:
    def __init__(self, SMS_multiviewApp):
        self.SMS_multiviewApp = SMS_multiviewApp
        self.texts = [sysinfo.imei(),
                      u"2"]
        self.listbox = appuifw.Listbox(self.texts, self.handle_select)

    def activate(self):
        appuifw.app.body = self.listbox
        appuifw.app.menu = [(u"Select", self.handle_select),
                            (u"Send", self.handle_send)]
        
    def handle_select(self):
        i = self.listbox.current()
        appuifw.note(u"Selected: " + self.get_text(),'info')

    def handle_send(self):
        appuifw.app.activate_tab(2)
        self.SMS_multiviewApp.handle_tab(2)

    def get_text(self):
        return self.texts[self.listbox.current()]


class TextView:
    def __init__(self, SMS_multiviewApp):
        self.SMS_multiviewApp = SMS_multiviewApp
        self.view_text = appuifw.Text()

    def activate(self):
        t = self.SMS_multiviewApp.get_text()
        self.view_text.set(t)
        appuifw.app.body = self.view_text
        appuifw.app.menu = [(u"Send", self.handle_send)]
        self.view_text.focus = True

    def handle_send(self):
        appuifw.app.activate_tab(2)
        self.SMS_multiviewApp.handle_tab(2)


class SendView:
    def __init__(self, SMS_multiviewApp):
        self.SMS_multiviewApp = SMS_multiviewApp
        self.log_text = appuifw.Text()
        self.log_contents = u""
        
    def activate(self):
        self.log_text.set(self.log_contents)
        appuifw.app.body = self.log_text
        appuifw.app.menu = []
       
        txt = self.SMS_multiviewApp.get_text()
        
        if appuifw.query(u"Send message to ?", 'query'):
            t = u"Sent " + txt + " \n"
            self.log_contents += t
            self.log_text.add(t)
            # messaging.sms_send(nbr, txt)
    

class SMS_multiviewApp:
    def __init__(self):
        self.lock = e32.Ao_lock()
        appuifw.app.exit_key_handler = self.exit_key_handler
        
        self.c_view = ChoiceView(self)
        self.t_view = TextView(self)
        self.s_view = SendView(self)
        self.views = [ self.c_view, self.t_view, self.s_view]
        appuifw.app.set_tabs([ u"Choice", u"Text", u"Send"],
                             self.handle_tab)
        
    def run(self):
        self.handle_tab(0)
        self.lock.wait()
        self.close()

    
    def get_text(self):
        return self.c_view.get_text()

    def handle_tab(self, index):
        self.views[index].activate()

    def exit_key_handler(self):
        self.lock.signal()

    def close(self):
        appuifw.app.exit_key_handler = None
        appuifw.app.set_tabs([u"Back to normal"], lambda x: None)
        del self.t_view
        del self.s_view

myApp = SMS_multiviewApp()
myApp.run()

appuifw.app.title = old_title
appuifw.menu = None
