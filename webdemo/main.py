__copyright__ = 'Copyright 2015 LaunchKey, Inc.  See project license for usage.'
__author__ = 'Adam Englander (adam@launchkey.com)'

import sys, sqlite3
from handlers import LaunchKeyHandler
from BaseHTTPServer import HTTPServer

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

    server = HTTPServer(('0.0.0.0', 8080), LaunchKeyHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    return server.serve_forever()

if __name__ == '__main__':
    sys.exit(main())
