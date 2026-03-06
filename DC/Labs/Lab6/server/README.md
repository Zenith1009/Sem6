# Lab 6 RMI Server Package

Run server side only:

```bash
docker build -t lab6-rmi-server .
docker run --rm -it --name lab6-rmi-server \
	-e RMI_HOSTNAME=<SERVER_DEVICE_IP> \
	-p 1099:1099 -p 2001:2001 \
	lab6-rmi-server
```

This starts `CatServer`, exposing:
- RMI registry: `1099`
- RMI object: `2001`

Serve file paths relative to server container `/app` (example: `sample.txt`).

If client is on another machine, set `RMI_HOSTNAME` to server machine IP.
