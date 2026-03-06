# Lab 6 RMI Client Package

Run client side only:

```bash
docker build -t lab6-rmi-client .
docker run --rm -it --name lab6-rmi-client lab6-rmi-client ./run_client.sh <SERVER_HOST> <FILENAME>
```

Example:

```bash
docker run --rm -it --name lab6-rmi-client lab6-rmi-client ./run_client.sh 192.168.1.20 sample.txt
```

If server is on same Mac host (not compose network), use `host.docker.internal` as server host.
