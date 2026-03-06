# Distributed Computing (CS332) | Assignment 6
## Java RMI CatServer/CatClient (Docker-Only Setup)

This lab implements `CatServer` and `CatClient` exactly as required in [Ques.md](Ques.md).

## Required Methods Implemented

- `openFile(String filename)`
- `nextLine()`
- `closeFile()`

## Folder Structure (shareable)

- [server/](server/) → share with teammate running server machine
- [client/](client/) → share with teammate running client machine
- [docker-compose.yml](docker-compose.yml) → one-machine two-container demo

## Docker two-container run (same machine)

From Lab6 root:

```bash
docker compose up -d --build rmi-server
docker compose run --rm -it rmi-client ./run_client.sh rmi-server sample.txt
```

Stop:

```bash
docker compose down
```

Full cleanup (optional):

```bash
docker compose down --remove-orphans
docker image rm lab6-rmi-server lab6-rmi-client 2>/dev/null || true
```

## Two-device sharing workflow (different machines)

### Server-side person

Share only [server/](server/), then run server container:

```bash
docker build -t lab6-rmi-server .
docker run --rm -it --name lab6-rmi-server \
	-e RMI_HOSTNAME=<SERVER_DEVICE_IP> \
	-p 1099:1099 -p 2001:2001 \
	lab6-rmi-server
```

### Client-side person

Share only [client/](client/), then run client container:

```bash
docker build -t lab6-rmi-client .
docker run --rm -it --name lab6-rmi-client lab6-rmi-client ./run_client.sh <SERVER_HOST> <FILENAME>
```

Example:

```bash
docker run --rm -it --name lab6-rmi-client lab6-rmi-client ./run_client.sh 192.168.1.20 sample.txt
```

If both client and server are on the same Mac host (without compose), use:

```bash
docker run --rm -it --name lab6-rmi-client lab6-rmi-client ./run_client.sh host.docker.internal sample.txt
```

If you already started server using `docker compose`, do not run another server container with same ports (`1099`, `2001`) at the same time.

## Notes

For cross-machine RMI, both server ports must be reachable and open in firewall/router:
- Registry port: `1099`
- Remote object port: `2001`

Do not run `docker compose` server and manual `docker run` server at the same time (port conflict on `1099`/`2001`).
