#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_server.sh
python3 src/pipeline_q8_collector.py --bind "${1:-tcp://*:5592}" --expected "${2:-20}"
