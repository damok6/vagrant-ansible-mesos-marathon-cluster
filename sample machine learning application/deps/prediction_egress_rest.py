__author__ = 'Damian Kelly'
__copyright__ = "Copyright 2016-2017, Damian Kelly"

import tornado.autoreload
import tornado.web
import tornado.httpserver
import os
# From http://stackoverflow.com/questions/2801882/generating-a-png-with-matplotlib-when-display-is-undefined:
# Force matplotlib to not use any Xwindows backend.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot
import cStringIO


global chosen_port
if 'PORT0' in os.environ:
    chosen_port = os.environ['PORT0']
else:
    chosen_port = 8889
print "Using port: " + str(chosen_port)


class RequestHandler(tornado.web.RequestHandler):
    # def initialize(self, kafka_producer):
    #     self.kafka_producer = kafka_producer

    page = """
    Simple Prediction Egress
    """

    def get(self, *args, **kwargs):
        # self.write(self.page)


        figdata = self.get_graph_bytes()

        self.set_header('Content-Type', 'image/png')
        self.write(figdata.getvalue())

    def get_graph_bytes(self):
        format = "png"
        figdata = cStringIO.StringIO()

        pyplot.plot([1, 2, 3, 4], [1, 3, 2, 4])
        pyplot.scatter([1, 2, 3, 4], [1, 2, 3, 4], color='g')

        pyplot.savefig(figdata, format=format)

        return figdata

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



