#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_server.sh
python3 src/pubsub_q4_q5_publisher.py --bind "${1:-tcp://*:5570}" --interval "${2:-1.0}"
