# sync.py
#

import appuifw
import phcomm
import os
import sys
import glob

class sync_client( phcomm.Client ):
    def __init__( self, sock, verbose=0 ):
        phcomm.Client.__init__( self, sock, verbose )
                            
    def run( self, with_reload = False ):
        old_title  = appuifw.app.title
        appuifw.app.title  = u'Sync files'

        # change current directory to Python home
        cwd = os.getcwd()
        if os.path.exists( 'c:/system/apps/python/python.app' ):
            os.chdir( 'c:/system/apps/python' )
        elif os.path.exists( 'e:/system/apps/python/python.app' ):
            os.chdir( 'e:/system/apps/python' )

        # ask for file names, checksums
        self.send( 'sync' )
        try:
            pc_offering = eval(self.recv_data())
        except 'Timeout':
            print 'BT connection timed out.'
            print 'Are you sure sync demon is running on PC?'
            return
        pc_demand   = eval(self.recv_data())
        # check whether some of the files should be retrieved
        for ph_file, pc_file, checksum in pc_offering:
            #print ph_file, pc_file
            if checksum != phcomm.file_checksum( ph_file ):
                # checksums differ, get the file
                self.send( 'getfile', pc_file )
                # create / overwrite the file
                dirpath = os.path.split( ph_file )[0]
                if not os.path.exists( dirpath ):
                    os.makedirs( dirpath ) 
                open( ph_file, 'wb' ).write( self.recv_data() )
                print 'received', ph_file

                if with_reload:
                    # reload a module if it appears in sys.modules
                    modpath, ext = os.path.splitext( ph_file )
                    modname = os.path.split(modpath)[1].lower()
                    if modname in sys.modules.keys():
                        reload( sys.modules[modname] )
                        print 'reloaded module: ', modname
            #else:
            #    print phcomm.file_checksum( ph_file ), checksum
       #print 'demand', pc_demand
        for targetdir, phone_patterns in pc_demand:
            if not isinstance(phone_patterns, tuple) and not isinstance(phone_patterns, list):
                # force patterns to be a list
                phone_patterns = [ phone_patterns ]
            for patt in phone_patterns:
                for fname in glob.glob( patt ):
                    try:
                        # assume if reading works, the rest works too
                        data = open( fname, 'rb' ).read()
                        crc = phcomm.data_checksum( data )
                        print 'offering', fname
                        self.send( 'offerfile %d' % crc )
                        self.send_data( os.path.join(targetdir, os.path.split(fname)[1]) )
                        if int(self.readline()):
                            self.send_data( data )
                            print '         SENT.'
                        else:
                            print '         NOT sent.'
                    except:
                        pass
        self.send( 'msg sync done.' )
        os.chdir( cwd )
        appuifw.app.title   = old_title
        
            
def main( interactive = True, with_reload = False ):
    sock = phcomm.connect_phone2PC( 'sync_conf.txt', interactive )
    if sock:
        try:
            #sync_client( sock, verbose=True ).run()
            sync_client( sock ).run( with_reload )
        except:
            print 'sync_client run failed'
            import traceback
            traceback.print_exc()
        print "Sync done."
    else:
        print 'Did not connect, exiting.'


if __name__ == '__main__':
    main()
#else:
#    main( False ) # for faster debugging, use the default host
