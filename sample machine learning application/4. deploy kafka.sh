# Must run with 
# source 4.\ deploy\ kafka.sh

if [[ -z "${MESOS_MASTER_IP}" ]]; then
  MESOS_MASTER_IP="192.168.33.20"
fi

echo "Deploying Kafka:"

curl -H "Content-Type: application/json" -X POST -d '
{
  "id": "/kafka",
  "cmd": "kafka_2.11-0.10.2.0/bin/kafka-server-start.sh kafka_2.11-0.10.2.0/config/server.properties --override zookeeper.connect=master:2181 --override port=$PORT0 --override auto.create.topics.enable=true",
  "cpus": 0.5,
  "mem": 256,
  "instances": 1,
  "uris": [
    "http://'${MESOS_MASTER_IP}'/file-server/kafka_2.11-0.10.2.0.tgz"
  ],
    "ports":[0]
}
' http://${MESOS_MASTER_IP}:8080/v2/apps


