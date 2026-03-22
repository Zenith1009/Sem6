#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_server.sh
python3 src/reqrep_q1_q2_server.py --bind "${1:-tcp://*:5555}"
