# Must run with 
# source 1.\ deploy\ file\ server.sh

# Will set Mesos master host IP only if it is not already set
if [[ -z "${MESOS_MASTER_IP}" ]]; then
  MESOS_MASTER_IP="192.168.33.20"
fi

curl -H "Content-Type: application/json" -X POST -d '
{
  "container": {
    "type": "DOCKER",
    "docker": {
	  "image": "tomsik68/xampp",
      "network": "BRIDGE",
      "portMappings": [
        { "containerPort": 22, "hostPort": 0, "servicePort": 0, "protocol": "tcp" },
		{ "containerPort": 80, "hostPort": 0, "servicePort": 0, "protocol": "tcp" }
      ]
    }
  },  
  "labels": {
    "HAPROXY_GROUP": "external",
    "HAPROXY_1_VHOST": "'${MESOS_MASTER_IP}'",
    "HAPROXY_1_HTTP_BACKEND_PROXYPASS_PATH": "/file-server",
    "HAPROXY_1_PATH":"/file-server"
  },
  "portDefinitions": [
    {
      "port": 0,
      "protocol": "tcp",
      "labels": {}
    }
  ],
  "id": "file-server",
  "instances": 1,
  "cpus": 0.25,
  "mem": 128
}' http://${MESOS_MASTER_IP}:8080/v2/apps
