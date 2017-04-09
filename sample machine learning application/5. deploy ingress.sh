# Must run with 
# source 5.\ deploy\ ingress.sh

if [[ -z "${MESOS_MASTER_IP}" ]]; then
  MESOS_MASTER_IP="192.168.33.20"
fi

echo "Deploying Ingress:"

curl -H "Content-Type: application/json" -X POST -d '
{
  "id": "/ingress",
  "cmd": "pip install -r data_ingress_rest_requirements.txt;python -u data_ingress_rest.py",
  "cpus": 0.2,
  "mem": 128,
  "instances": 2,
  "uris": [
    "http://'${MESOS_MASTER_IP}'/file-server/data_ingress_rest.py",
	"http://'${MESOS_MASTER_IP}'/file-server/data_ingress_rest_requirements.txt"
  ],
  "ports":[0],
  "labels": {
	"HAPROXY_GROUP": "external",
	"HAPROXY_0_VHOST": "'${MESOS_MASTER_IP}'",
    "HAPROXY_0_HTTP_BACKEND_PROXYPASS_PATH": "/ingress",
	"HAPROXY_0_PATH":"/ingress"
  }
}
' http://${MESOS_MASTER_IP}:8080/v2/apps


