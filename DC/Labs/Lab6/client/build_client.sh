#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

javac CatService.java CatClient.java

echo "Client build complete"
