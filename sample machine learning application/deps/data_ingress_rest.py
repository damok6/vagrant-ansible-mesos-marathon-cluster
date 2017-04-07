__author__ = 'Damian Kelly'
__copyright__ = "Copyright 2016-2017, Damian Kelly"

import tornado.autoreload
import tornado.web
import tornado.httpserver
import time
from json import dumps
import os

global chosen_port
if 'PORT0' in os.environ:
    chosen_port = os.environ['PORT0']
else:
    chosen_port = 8889
print "Using port: " + str(chosen_port)


class RequestHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("""
Sample Data Pusher.<br>
Internal Server Port = """+str(chosen_port)+"""
""")

def main():

    applicaton = tornado.web.Application([
        (r"/(.*)", RequestHandler, {}),
    ],
        autoreload=True)

    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(chosen_port)
    tornado.ioloop.IOLoop.instance().start()#

if __name__ == '__main__':
    print 'Start'
    main()