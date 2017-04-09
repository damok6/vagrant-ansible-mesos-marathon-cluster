__author__ = 'Damian Kelly'
__copyright__ = "Copyright 2016-2017, Damian Kelly"

import tornado.autoreload
import tornado.web
import tornado.httpserver
import json
import requests
import os
import kafka

global chosen_port
if 'PORT0' in os.environ:
    chosen_port = os.environ['PORT0']
else:
    chosen_port = 8889
print "Using port: " + str(chosen_port)


class RequestHandler(tornado.web.RequestHandler):

    def initialize(self, kafka_producer):
        self.kafka_producer = kafka_producer

    page = """
    Sample Data Pusher.<br>
    Internal Server Port = """ + str(chosen_port) + """
    <form method = "post">
        <input type="submit" name="upvote" value="Post Data" />
    </form>
    """

    def get(self, *args, **kwargs):
        self.write(self.page)

    def post(self, *args, **kwargs):
        print "Post data over Kafka"
        self.kafka_producer.send('test', b'some_message_bytes')
        self.write(self.page)

def main():

    request_text = requests.get('http://master:8123/v1/services/_kafka._tcp.marathon.slave.mesos.').text
    request_dict = json.loads(request_text)

    # get the settings for only 1 broker for now:
    bootstrap_servers = [request_dict[0]['ip'] + ':' + request_dict[0]['port']]
    print bootstrap_servers
    kafka_producer = kafka.KafkaProducer(bootstrap_servers=bootstrap_servers)

    applicaton = tornado.web.Application([
        (r"/(.*)", RequestHandler, {"kafka_producer":kafka_producer}),
    ],
        autoreload=True)

    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(chosen_port)
    tornado.ioloop.IOLoop.instance().start()#

if __name__ == '__main__':
    print 'Start'
    main()
