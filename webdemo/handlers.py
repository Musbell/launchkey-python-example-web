import socket

__author__ = 'adam'

from BaseHTTPServer import BaseHTTPRequestHandler


import os, urlparse, pystache, cgi, time
from pkg_resources import resource_filename

class LaunchKeyHandler(BaseHTTPRequestHandler, object):

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
        self.close_connection = 1

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

        elif form.has_key('deorbit'):
            if auth_request:
                self.launchkey.logout(auth_request)
                self.sqlite.execute('DELETE FROM auth WHERE request = ?', (auth_request,))
                self.sqlite.commit()
            self.send_response(302)
            self.send_header("location", "/")

        elif query.has_key('auth') and query.has_key('auth_request') and query.has_key('user_hash'):
            auth_request = query.get('auth_request').pop()
            authorized = self.launchkey.is_authorized(auth_request, query.get('auth').pop())
            self.sqlite.execute(
                'UPDATE auth SET status = ?, userhash = ? where request = ?',
                (2 if authorized else 0, query.get('user_hash').pop(), auth_request)
            )
            self.sqlite.commit()
            self.send_response(200)

        elif query.has_key('deorbit') and query.has_key('signature'):
            user_hash = self.launchkey.deorbit(query.get('deorbit').pop(), query.get('signature').pop())
            if user_hash:
                code = 200
                c = self.sqlite.cursor()
                c.execute('SELECT request FROM auth WHERE userhash = ?', (user_hash,))
                for row in c.fetchall():
                    try:
                        request = row[0]
                        self.sqlite.execute('DELETE FROM auth WHERE request = ?', (request,))
                        self.sqlite.commit()
                        self.launchkey.logout(request)
                    except:
                        pass


            else:
                code = 400

            self.send_response(code)

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
        filename = resource_filename(__name__, '../static/favicon.ico')

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

    def __get_auth_request_cookie(self):
        cookie_string = self.headers.getheader('Cookie')
        if cookie_string is not None:
            cookies = cookie_string.split(";")
            for cookie in cookies:
                (key, value) = cookie.strip().split("=")
                if key.strip() == 'AuthRequest':
                    return value

