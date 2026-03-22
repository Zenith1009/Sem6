#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_client.sh
python3 src/pubsub_q6_dynamic_subscriber.py --endpoints "${1:-tcp://localhost:5581,tcp://localhost:5582,tcp://localhost:5583}" --topics "${2:-SPORTS}"
