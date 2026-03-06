#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

rpcgen -C lab5.x

gcc -Wall -Wextra -O2 -I/usr/include/tirpc -o lab5_client \
  lab5_client.c lab5_clnt.c lab5_xdr.c -ltirpc -lm

echo "Client build complete: ./lab5_client"
