#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_client.sh
python3 src/pipeline_q9_aggregator.py --bind "${1:-tcp://*:5602}" --name "${2:-agg-1}" --expected "${3:-0}"
