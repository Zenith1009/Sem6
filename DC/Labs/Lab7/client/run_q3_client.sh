#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_client.sh
python3 src/reqrep_q3_client.py --endpoint "${1:-tcp://localhost:5560}" --count "${2:-5}" --name "${3:-client-A}"
