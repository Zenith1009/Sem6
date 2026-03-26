# Lab 8 Observation Notes

Use this file to paste your command outputs/screenshots and finalize submission.

## Q2
- `docker run hello-world` (or equivalent image) succeeded.
- Running containers listed with `docker ps`.
- All containers listed with `docker ps -a`.

## Q4
- Both containers joined custom network.
- Name-based communication succeeded (`ping container-name`).
- Container IPs verified using `docker inspect`.

## Q5
- Single pod reached `Running` state.
- Pod IP visible in `kubectl get pod -o wide`.

## Q6
- Multiple pods had different IPs.
- Deleting and recreating pod changed IP (in most runs).

## Q7
- Tester pod could access web pod directly via pod IP.

## Q8
- Tester pod could access web app via service DNS name (`web-svc`).
- Service-based access remained stable compared to direct Pod IP.
