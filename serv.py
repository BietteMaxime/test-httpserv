import BaseHTTPServer
import cgi
import json
import urlparse

import app_serv

__author__ = 'Maxime'


dispatcher = app_serv.Dispatcher([
    {'name': 'MyName', 'outer_name': 'WhatOthersCallMe', 'location': 'APlace'},
    {'name': 'MyName2', 'outer_name': 'WhatOthersCallMe2', 'location': 'APlace'}

])


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/":
            self.send_error(404)
            return
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        print ctype
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        postvars['outer_name'] = dispatcher.post(postvars)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(postvars))

    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write('''
<html>
    <body>
        <h1>This is the beginning of a nice adventure.</h1>
        <form method="POST" action="/" enctype="multipart/form-data">
            <input type="text" name="name" />
            <input type="text" name="test" />
            <input type="submit" value="Submit">
        </form>
    </body>
</html>
''')


def run(server_class=BaseHTTPServer.HTTPServer, handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run(handler_class=MyHandler)
