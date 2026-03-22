#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_client.sh
python3 src/pipeline_q9_stage2_worker.py --input-endpoint "${1:-tcp://localhost:5600}" --output-endpoints "${2:-tcp://localhost:5602}" --worker-id "${3:-s2-worker-1}" --process-delay "${4:-0.03}"
