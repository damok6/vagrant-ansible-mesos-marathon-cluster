# Based on example here:
# https://github.com/apache/spark/blob/master/examples/src/main/python/streaming/kafka_wordcount.py

#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
 To run this on your local machine, you need to setup Kafka and create a producer first, see
 http://kafka.apache.org/documentation.html#quickstart
 and then run with:

 spark-2.1.0-bin-hadoop2.7/bin/spark-submit --jars \
    spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar \
    spark_streaming_kafka_consumer.py \
    master:2181/kafka test

"""
from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json
import requests
from cassandra.cluster import Cluster
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import pickle

# import pip
# pip.main(['install', 'cql'])
# import cql

def handle_incoming_data(data):
    data_list = [json.loads(sample) for sample in data]
    print(data_list)

    cass_ip, cass_port = get_cassandra_details()

    generate_store_model_samples(current_sample_list=data_list,
                                 cass_ip=cass_ip,
                                 cass_port=cass_port)

    return data


def get_cassandra_details():
    request_text = requests.get('http://master:8123/v1/services/_cassandra._tcp.marathon.slave.mesos.').text
    request_dict = json.loads(request_text)

    cass_ip = request_dict[0]['ip']
    cass_port = request_dict[0]['port']

    return cass_ip, cass_port


def generate_store_model_samples(current_sample_list, cass_ip, cass_port):
    """
    gets all samples currently in database
    generates model
    stores model
    stores only the recently received samples
    """
    cluster = Cluster([cass_ip], int(cass_port))
    session = cluster.connect()
    # NOTE: None of these schema represent the best practice in Casandra schema design,
    # they are merely for simple examples:
    session.execute("CREATE KEYSPACE IF NOT EXISTS ml_db WITH "
                    "REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1}")
    session.set_keyspace('ml_db')
    session.execute("CREATE TABLE IF NOT EXISTS all_raw_data"
                    "(time timeuuid PRIMARY KEY, samples text)")
    session.execute("CREATE TABLE IF NOT EXISTS models"
                    "(time timeuuid, model_id int, model text, PRIMARY KEY(model_id, time))")

    rows = session.execute('SELECT samples FROM all_raw_data')
    all_data = [json.loads(row.samples) for row in rows]

    # Insert the new samples into the database, while appending the samples on the currently loaded list:
    prepared = session.prepare("""INSERT INTO all_raw_data(time, samples) VALUES (now(), ?)""")
    for sample in current_sample_list:
        session.execute(prepared.bind((json.dumps(sample),)))
        all_data.append(sample)

    # Train the model:
    X = []
    y = []
    for sample in all_data:
        X.append([sample[1]])
        y.append(sample[0])

    model = Pipeline([('poly', PolynomialFeatures(degree=2)),
                      ('linear', LinearRegression(fit_intercept=False))])

    model.fit(X, y)

    print(all_data)
    print(X)
    print(y)
    print(model.predict([[35]]))
    # print(pickle.dumps(model, 1))

    prepared = session.prepare("""INSERT INTO models(time, model_id, model) VALUES (now(), 1, ?)""")
    session.execute(prepared.bind((pickle.dumps(model, 0),)))

    cluster.shutdown()

def non_streaming_test():
    test_data = [
        [0.9162945682034958, 22.354928807291714],
        [0.9143165408602164, 44.43175529222497],
        [0.8712083920269407, 25.33219157304891]
    ]

    cass_ip, cass_port = get_cassandra_details()

    generate_store_model_samples(current_sample_list=test_data,
                                 cass_ip=cass_ip,
                                 cass_port=cass_port)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: spark_streaming_kafka_consumer.py <zk> <topic>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="PythonStreamingKafka")  # , pyFiles=['spark_utils.py']
    ssc = StreamingContext(sc, 3)

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    # Combine all samples into one sample list and pipe through the handle_incoming_data function:
    lines = kvs.map(lambda x: x[1])
    counts = lines.map(lambda sample: (1, [sample])) \
        .reduceByKey(lambda a, b: a+b)\
        .map(lambda x: x[1])\
        .map(handle_incoming_data)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
