# Lab5 RPC Client Package

Share this `client/` folder with the teammate who will run the client machine.

## Run

```bash
docker build -t lab5-rpc-client ./client
docker run --rm -it --name lab5-rpc-client lab5-rpc-client ./run_client.sh <SERVER_HOST> <SERVER_PORT>
```

Example:

```bash
docker run --rm -it --name lab5-rpc-client lab5-rpc-client ./run_client.sh 192.168.1.20 50051
```

`<SERVER_HOST>` should be the server machine IP/hostname reachable from client machine. Use the same UDP port that the server was started with.
