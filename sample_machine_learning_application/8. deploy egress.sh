# Must run with 
# source 8.\ deploy\ egress.sh

if [[ -z "${MESOS_MASTER_IP}" ]]; then
  MESOS_MASTER_IP="192.168.33.20"
fi

echo "Deploying Egress:"

curl -H "Content-Type: application/json" -X POST -d '
{
  "id": "/egress",
  "cmd": "pip install -r prediction_egress_rest_requirements.txt;python -u prediction_egress_rest.py",
  "cpus": 0.2,
  "mem": 128,
  "instances": 2,
  "uris": [
    "http://'${MESOS_MASTER_IP}'/file-server/prediction_egress_rest.py",
	"http://'${MESOS_MASTER_IP}'/file-server/prediction_egress_rest_requirements.txt"
  ],
  "ports":[0],
  "labels": {
	"HAPROXY_GROUP": "external",
	"HAPROXY_0_VHOST": "'${MESOS_MASTER_IP}'",
    "HAPROXY_0_HTTP_BACKEND_PROXYPASS_PATH": "/egress",
	"HAPROXY_0_PATH":"/egress"
  }
}
' http://${MESOS_MASTER_IP}:8080/v2/apps


