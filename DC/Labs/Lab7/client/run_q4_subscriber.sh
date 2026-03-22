#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_client.sh
python3 src/pubsub_q4_subscriber.py --endpoint "${1:-tcp://localhost:5570}" --tag "${2:-TIME}"
