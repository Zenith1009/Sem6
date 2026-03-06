#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_client.sh

SERVER_HOST="${1:-127.0.0.1}"
SERVER_PORT="${2:-50051}"
echo "Connecting to RPC server: ${SERVER_HOST}:${SERVER_PORT} (UDP)"
./lab5_client "${SERVER_HOST}" "${SERVER_PORT}"
