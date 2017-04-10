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
import requests
import json
from cassandra.cluster import Cluster
import numpy as np
import pickle

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
        self.finish()

    def get_graph_bytes(self):
        format = "png"
        figdata = cStringIO.StringIO()

        model_x, model_y, data_x, data_y = self.get_model_data()
        pyplot.plot(model_x, model_y)
        pyplot.scatter(data_x, data_y, color='g')

        pyplot.savefig(figdata, format=format)
        pyplot.close()

        return figdata

    def get_model_data(self):
        model_x = []
        model_y = []
        data_x = []
        data_y = []

        request_text = requests.get('http://master:8123/v1/services/_cassandra._tcp.marathon.slave.mesos.').text
        request_dict = json.loads(request_text)

        cass_ip = request_dict[0]['ip']
        cass_port = request_dict[0]['port']

        cluster = Cluster([cass_ip], int(cass_port))
        session = cluster.connect()
        session.set_keyspace('ml_db')
        rows = session.execute('select model from models where model_id=1 order by time desc limit 1')
        for row in rows:
            model_pickle = row.model
            model = pickle.loads(model_pickle)
            model_x = np.linspace(0, 70, 71)
            model_y = model.predict([[x] for x in model_x])

        rows = session.execute('select samples from all_raw_data')
        for row in rows:
            sample = json.loads(row.samples)
            data_x.append(sample[1])
            data_y.append(sample[0])

        session.shutdown()

        return model_x, model_y, data_x, data_y


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



