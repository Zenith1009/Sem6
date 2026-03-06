#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_client.sh

SERVER_HOST="${1:-rmi-server}"
FILENAME="${2:-sample.txt}"

echo "Connecting to RMI server at ${SERVER_HOST}:1099 for file ${FILENAME}"
java \
	-Dsun.rmi.transport.connectionTimeout=5000 \
	-Dsun.rmi.transport.tcp.responseTimeout=5000 \
	CatClient "$SERVER_HOST" "$FILENAME"
