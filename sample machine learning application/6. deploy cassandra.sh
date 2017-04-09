# Must run with 
# source 6.\ deploy\ cassandra.sh

# Will set Mesos master host IP only if it is not already set
if [[ -z "${MESOS_MASTER_IP}" ]]; then
  MESOS_MASTER_IP="192.168.33.20"
fi

curl -H "Content-Type: application/json" -X POST -d '
{
  "container": {
    "type": "DOCKER",
    "docker": {
	  "image": "cassandra:2",
      "network": "BRIDGE",
      "portMappings": [
        { "containerPort": 9042, "hostPort": 0, "servicePort": 0, "protocol": "tcp" }      ]
    }
  },  
  "id": "cassandra",
  "instances": 1,
  "cpus": 0.25,
  "mem": 512

}' http://${MESOS_MASTER_IP}:8080/v2/apps
