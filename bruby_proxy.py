#!/usr/bin/env python
# coding: utf-8
"""
Very simple HTTP server in python.
This is a hacked down version of a server to act as a proxy for the bigger rails / react version on heroku.
Usage: python bruby-proxy.py 80
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from urlparse import urlparse
import urllib2
from time import gmtime, strftime

logStamp=strftime("%Y%m%d", gmtime())
apiLog = './logs/%s_API_CALLS.txt' % logStamp

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        ignoreArray=('/favicon.ico','/apple-touch-icon-precomposed.png','/apple-touch-icon.png')
        if parsed.path in ignoreArray: #filter for favicon requests chrome and safari
            pass
        else:
            print "get req is %s" % parsed.path
            print "parsed.query is %s" % parsed.query
            url = ('https://bruby-app.herokuapp.com%s?%s' % (parsed.path, parsed.query))
            print url
            response = urllib2.urlopen(url)
            html = response.read()
            print html
            self._set_headers()
            self.wfile.write(html) #this sends the server response
            print ("sent response")
            try:
                with open(apiLog, "a") as text_file:
                    text_file.write("r %s \nc %s \n \n" % (html, parsed.path)) #write api response to log
            except:
                print ("error writing apiLog call")
    def do_HEAD(self):
        self._set_headers()

    def do_POST(self): # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    print """
 _______  ______    _     _  _______  __   __
|  _    ||    _ |  | |   | ||  _    ||  | |  |
| |_|   ||   | ||  | |   | || |_|   ||  |_|  |
|       ||   |_||_ | |   | ||       ||       |
|  _   | |    __  || |   | ||  _   | |_     _|
| |_|   ||   |  | || |___| || |_|   |  |   |
|_______||___|  |_||_______||_______|  |___| """
    print '01 start this server as sudo on port 80 -> "python sudo bruby-proxy.py 80"'
    print '02 start internet sharing'
    print '03 set dnsmasq to address=/targetURL.com/your.actual.ip.address'
    print '*** note - use the ip of the shared connection (WIFI, not connected to your router)'
    print '04 reset the dns server with'
    print '"sudo launchctl stop homebrew.mxcl.dnsmasq"'
    print '"sudo launchctl start homebrew.mxcl.dnsmasq"'
    print '05 these commands should give you info on the redirect.'
    print '"dig @127.0.0.1 +short targetURL.com" and "nslookup targetURL.com"'
    print 'Have a great brew!'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
