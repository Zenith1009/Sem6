#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

javac CatService.java CatServiceImpl.java CatServer.java

echo "Server build complete"
