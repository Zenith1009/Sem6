#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

CATEGORY="${1:-SPORTS}"
BIND="${2:-tcp://*:5581}"
INTERVAL="${3:-1.0}"

./build_server.sh
python3 src/pubsub_q6_publisher.py --category "$CATEGORY" --bind "$BIND" --interval "$INTERVAL"
