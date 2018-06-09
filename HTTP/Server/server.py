#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver, time, datetime

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

  # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
 
        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    def do_POST(self):
        print("HEADERS: ")
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        print(self)
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print(post_data) # <-- Print post data
        self._set_headers()

def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    #Se estiver executando em localhost, usar o codigo abaixo pra obter o IP
    ip = ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr']
    # print("meu ip em wlp3s0 é: {}".format(ip))
    #Se estiver executando em rede, usar o codigo abaixo pra obter o IP
    # ip = ni.ifaddresses('enp9s0')[ni.AF_INET][0]['addr']
    # print("meu ip em enp9s0 é: {}".format(ip))

    print('Iniciando servidor HTTP em {}:{}...\n'.format(ip, port))
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    import netifaces as ni
    print(ni.interfaces())


    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()