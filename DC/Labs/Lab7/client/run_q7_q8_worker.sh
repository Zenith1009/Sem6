#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_client.sh
python3 src/pipeline_q7_q8_worker.py --input-endpoint "${1:-tcp://localhost:5590}" --collector-endpoint "${2:-}" --worker-id "${3:-worker-1}"
