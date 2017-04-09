# Must run with 
# source 2.\ get\ dependencies.sh

if [[ -z "${MESOS_MASTER_IP}" ]]; then
  MESOS_MASTER_IP="192.168.33.20"
fi

cd deps

curl -O http://mirrors.whoishostingthis.com/apache/kafka/0.10.2.0/kafka_2.11-0.10.2.0.tgz
curl -O http://d3kbcqa49mib13.cloudfront.net/spark-2.1.0-bin-hadoop2.7.tgz
curl -O http://central.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-8-assembly_2.11/2.1.0/spark-streaming-kafka-0-8-assembly_2.11-2.1.0.jar

cd ..