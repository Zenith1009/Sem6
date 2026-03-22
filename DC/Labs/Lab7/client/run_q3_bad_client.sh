#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_client.sh
python3 src/reqrep_q3_bad_client.py --endpoint "${1:-tcp://localhost:5560}"
