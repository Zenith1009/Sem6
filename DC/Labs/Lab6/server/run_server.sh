#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

./build_server.sh
java CatServer
