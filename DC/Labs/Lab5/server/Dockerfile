FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential rpcbind rpcsvc-proto libtirpc-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN chmod +x /app/build_server.sh /app/run_server.sh

CMD ["bash", "-lc", "./run_server.sh"]
