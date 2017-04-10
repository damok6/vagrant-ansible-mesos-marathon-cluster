# Must run with
# source 5.\ deploy\ spark\ streaming\ consumer.sh

if [[ -z "${MESOS_MASTER_IP}" ]]; then
  MESOS_MASTER_IP="192.168.33.20"
fi

echo "Deploying Spark Kafka Streaming Consumer:"

curl -H "Content-Type: application/json" -X POST -d '
{
  "id": "/streaming-consumer",
  "cmd": "spark-2.1.0-bin-hadoop2.7/bin/spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar spark_streaming_kafka_consumer.py master:2181/kafka test",
  "cpus": 0.5,
  "mem": 128,
  "instances": 1,
  "uris": [
    "http://'${MESOS_MASTER_IP}'/file-server/spark_streaming_kafka_consumer.py",
	"http://'${MESOS_MASTER_IP}'/file-server/spark-2.1.0-bin-hadoop2.7.tgz",
	"http://'${MESOS_MASTER_IP}'/file-server/spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar"
  ]
}' http://${MESOS_MASTER_IP}:8080/v2/apps
