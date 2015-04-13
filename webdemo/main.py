__copyright__ = 'Copyright 2015 LaunchKey, Inc.  See project license for usage.'
__author__ = 'Adam Englander (adam@launchkey.com)'

import sys, sqlite3, socket
from launchkey import API
from handlers import LaunchKeyHandler
from BaseHTTPServer import HTTPServer

class CleanServer(HTTPServer):
    def finish_request(self, request, client_address):
        '''
        Catch broken pipe errors for finish request.  They have no bearing here and simple upset people for no reason.
        :return:
        '''
        try:
            HTTPServer.finish_request(self, request, client_address)
        except socket.error, e:
            if e.errno == 32: # 32 is broken pipe
                pass
            else:
                raise e



def main():
    '''
    Main method that creates and runs app
    :param argv:
    :return:
    '''
    # db_file = resource_filename(__name__, 'data.sq3')
    db_file = ':memory:'
    LaunchKeyHandler.sqlite = sqlite3.connect(db_file)
    LaunchKeyHandler.sqlite.execute('CREATE TABLE IF NOT EXISTS auth(request UNIQUE, status INT, timestamp INT, userhash)')

    args = sys.argv[1:]
    if len(args) != 3:
        print "\n\n"
        print "Usage:\n"
        print "    launchkeywebdemo app_key secret_key pk_location"
        print ""
        print "    app_key:     Your application's key"
        print "    secret_key:  Your application's secret key"
        print "    pk_location: The location of your application's RSA private key"
        print "\n\n"
        return

    app_key = args[0]
    secret_key = args[1]
    private_key_location = args[2]
    private_key = file(private_key_location).read()
    LaunchKeyHandler.launchkey = API(app_key, secret_key, private_key)

    server = CleanServer(('0.0.0.0', 8080), LaunchKeyHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    return server.serve_forever()

if __name__ == '__main__':
    sys.exit(main())
