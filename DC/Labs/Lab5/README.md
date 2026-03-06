# Distributed Computing (CS332) | Assignment 5
## Two-Person RPC Setup (Separate Client/Server Folders + Separate Containers)

This implementation follows [Ques.md](Ques.md) and is organized for a two-student, two-role workflow.

## Implemented RPC Procedures

1. Palindrome check
2. Leap year check
3. GCD
4. Square root
5. Swap without third variable
6. Max/Min/Average of array
7. Compare two strings
8. Substring check
9. Concatenate strings
10. Reverse array

## Folder Structure for Sharing

- [server/](server/) → share this folder with teammate handling server
- [client/](client/) → share this folder with teammate handling client
- [docker-compose.yml](docker-compose.yml) → local two-container testing on one machine

Each folder is self-contained with its own:
- `lab5.x`
- source code
- build script
- run script
- Dockerfile

## Local Demo (single machine, two containers)

From Lab5 root:

```bash
docker compose up -d --build rpc-server
docker compose run --rm -it rpc-client ./run_client.sh rpc-server 50051
```

Stop:

```bash
docker compose down
```

Full cleanup (optional):

```bash
docker compose down --remove-orphans
docker image rm lab5-rpc-server lab5-rpc-client 2>/dev/null || true
```

## Real Two-Device Usage

This project is configured for direct UDP RPC on a fixed port (default `50051`) so it does not depend on host port `111`.

### Server-side person

Share only [server/](server/) and run:

```bash
docker build -t lab5-rpc-server ./server
docker run --rm -it --name lab5-rpc-server -p 50051:50051/udp lab5-rpc-server ./run_server.sh 50051
```

### Client-side person

Share only [client/](client/) and run:

```bash
docker build -t lab5-rpc-client ./client
docker run --rm -it --name lab5-rpc-client lab5-rpc-client ./run_client.sh <SERVER_HOST> 50051
```

Example:

```bash
docker run --rm -it --name lab5-rpc-client lab5-rpc-client ./run_client.sh 192.168.1.20 50051
```

## Important Note

Allow inbound UDP on the chosen port (default `50051`) in host firewall/network settings.
