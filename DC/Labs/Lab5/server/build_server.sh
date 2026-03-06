#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

rpcgen -C lab5.x

gcc -Wall -Wextra -O2 -I/usr/include/tirpc -o lab5_server \
  lab5_fixed_server.c lab5_server.c lab5_xdr.c -ltirpc -lm

echo "Server build complete: ./lab5_server"
