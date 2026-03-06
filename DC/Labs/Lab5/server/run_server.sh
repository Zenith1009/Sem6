#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_server.sh

RPC_PORT="${1:-${RPC_PORT:-50051}}"

echo "Starting LAB5 RPC server on UDP port ${RPC_PORT}..."
./lab5_server "${RPC_PORT}"
