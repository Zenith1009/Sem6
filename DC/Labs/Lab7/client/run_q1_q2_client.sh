#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_client.sh
ENDPOINT="${1:-tcp://localhost:5555}"
STOP="${2:-no}"

if [[ "$STOP" == "stop" ]]; then
	python3 src/reqrep_q1_q2_client.py --endpoint "$ENDPOINT" --stop-server
else
	python3 src/reqrep_q1_q2_client.py --endpoint "$ENDPOINT"
fi
