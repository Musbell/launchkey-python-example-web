__author__ = 'adam'

from BaseHTTPServer import BaseHTTPRequestHandler


import os, sys, urlparse, pystache, sqlite3, cgi, time, logging
from launchkey import API
from pkg_resources import resource_filename

class LaunchKeyHandler(BaseHTTPRequestHandler):
    sqlite = None
    launchkey = None

    def __init__(self, request, client_address, server):

        db_file = resource_filename(__name__, 'data.sq3')
        logging.info('Using SQLite DB file %s' % (db_file))
        self.sqlite = sqlite3.connect(db_file)
        self.sqlite.execute('CREATE TABLE IF NOT EXISTS auth(request UNIQUE, status INT, timestamp INT, userhash)')

        args = sys.argv[1:]
        app_key = args[0]
        secret_key = args[1]
        private_key_location = args[2]
        private_key = file(private_key_location).read()
        self.launchkey = API(app_key, secret_key, private_key)
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def __get_status(self, auth_request):
        status = 0
        if auth_request is not None and not auth_request == '':
            c = self.sqlite.cursor()
            c.execute('SELECT status FROM auth WHERE request = ? LIMIT 1', (auth_request,));
            row = c.fetchone()
            if row:
                (status,) = row
            c.close()
        return status

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        if parsed_path.path == '/favicon.ico':
            return self.__serve_favicon()

        auth_request = self.__get_auth_request_cookie()
        status = self.__get_status(auth_request)

        template = file(os.path.join(os.path.dirname(__file__), '..', 'templates', 'template.html')).read()

        context = {
            "unauthorized": True if status < 1 else None,
            "authorized": True if status == 2 else None,
            "authorizing": True if status == 1 else None,
        }

        page = pystache.render(template, context)
        self.send_response(200)
        self.send_header("Set-Cookie", "AuthRequest=%s" % (auth_request if auth_request is not None else ''))
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        parsed_path = urlparse.urlparse(self.path)
        auth_request = self.__get_auth_request_cookie()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers.get('Content-Type'),}
        )

        query = urlparse.parse_qs(parsed_path.query)
        if form.has_key('username'):
            username = form.getvalue('username')
            auth_request = self.launchkey.authorize(username, True)
            status = 1
            self.sqlite.execute(
                'INSERT OR REPLACE INTO auth (request, status, timestamp) VALUES (?, ?, ?)',
                (auth_request, status, time.time())
            )
            self.sqlite.commit()
            self.send_response(302)
            self.send_header("Set-Cookie", "AuthRequest=%s" % (auth_request))
            self.send_header("location", "/")
            self.end_headers()
            return
        elif form.has_key('deorbit'):
            if auth_request:
                self.launchkey.logout(auth_request)
                self.sqlite.execute('DELETE FROM auth WHERE request = ?', (auth_request,))
                self.sqlite.commit()
            self.send_response(302)
            self.send_header("location", "/")
            self.end_headers()
            return
        elif query.has_key('auth') and query.has_key('auth_request') and query.has_key('user_hash'):
            auth_request = query.get('auth_request').pop()
            authorized = self.launchkey.is_authorized(auth_request, query.get('auth').pop())
            self.sqlite.execute(
                'UPDATE auth SET status = ?, userhash = ? where request = ?',
                (2 if authorized else 0, query.get('user_hash').pop(), auth_request)
            )
            self.sqlite.commit()
            self.send_response(302)
            self.send_header("location", "/")
            self.end_headers()
            return
        elif query.has_key('deorbit') and query.has_key('signature'):
            user_hash = self.launchkey.deorbit(query.get('deorbit').pop(), query.get('signature').pop())
            if user_hash:
                code = 200
                self.sqlite.execute('DELETE FROM auth WHERE userhash = ?', (user_hash,))
                self.sqlite.commit()
            else:
                code = 400

            self.send_response(code)
            self.end_headers()
            return
        else:
            status = self.__get_status(auth_request)
            if status == 2:
                code = 200
            elif status == 1:
                code = 401
            else:
                code = 403

            self.send_response(code)
            self.end_headers()
            return

    def __serve_favicon(self):
        filename = os.path.join(os.path.dirname(__file__), 'favicon.ico')

        self.send_response(200)
        self.send_header('Content-Type', 'image/x-icon')
        self.send_header('Content-Length', os.stat(filename).st_size)
        self.end_headers()

        icofile = file(filename)
        while True:
            chunk = icofile.read(256)
            if chunk:
                self.wfile.write(chunk)
            else:
                icofile.close()
                return

    def __get_auth_request_cookie(self):
        cookie_string = self.headers.getheader('Cookie')
        if cookie_string is not None:
            cookies = cookie_string.split(";")
            for cookie in cookies:
                (key, value) = cookie.strip().split("=")
                if key.strip() == 'AuthRequest':
                    return value

