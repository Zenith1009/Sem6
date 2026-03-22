#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_server.sh
python3 src/reqrep_q3_worker.py --backend-endpoint "${1:-tcp://localhost:5561}" --worker-id "${2:-worker-1}"
