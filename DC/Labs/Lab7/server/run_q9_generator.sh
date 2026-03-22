#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_server.sh
python3 src/pipeline_q9_generator.py --bind "${1:-tcp://*:5600}" --tasks "${2:-50}" --delay "${3:-0.01}"
