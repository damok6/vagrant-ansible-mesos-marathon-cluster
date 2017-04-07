# Must run with 
# source 3.\ upload\ dependencies.sh

if [[ -z "${MESOS_MASTER_IP}" ]]; then
  MESOS_MASTER_IP="192.168.33.20"
fi

echo "Discovering file server host IP and port:"

export PYTHONIOENCODING=utf8
IP=$(curl -s 'http://'${MESOS_MASTER_IP}':8123/v1/services/_file-server._tcp.marathon.slave.mesos.' | \
    python -c "import sys, json
resp_dict=json.load(sys.stdin)
print resp_dict[0]['ip']
")

PORT=$(curl -s 'http://'${MESOS_MASTER_IP}':8123/v1/services/_file-server._tcp.marathon.slave.mesos.' | \
    python -c "import sys, json
resp_dict=json.load(sys.stdin)
all_ports=[entry['port'] for entry in resp_dict]
print min(all_ports)
")

echo $IP
echo $PORT

echo "Uploading dependencies to server:"

cmd='scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P '$PORT' deps/* root@'$IP':/opt/lampp/htdocs/'
$cmd

echo ""
echo "Done, files are now available at:"

for f in deps/*
do
    echo '  http://'${MESOS_MASTER_IP}'/file-server/'$(basename $f)
done