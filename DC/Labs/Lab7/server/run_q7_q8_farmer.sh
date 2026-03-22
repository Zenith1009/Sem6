#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_server.sh
python3 src/pipeline_q7_q8_farmer.py --bind "${1:-tcp://*:5590}" --tasks "${2:-20}" --delay "${3:-0.05}"
