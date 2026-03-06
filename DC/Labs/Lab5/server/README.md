# Lab5 RPC Server Package

Share this `server/` folder with the teammate who will run the server machine.

## Run

```bash
docker build -t lab5-rpc-server ./server
docker run --rm -it --name lab5-rpc-server -p 50051:50051/udp lab5-rpc-server ./run_server.sh 50051
```

The server listens on UDP port `50051` by default (or any port you pass).

## Note
Allow inbound UDP on the chosen port in firewall settings.
