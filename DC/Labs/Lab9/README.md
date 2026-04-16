# Distributed Computing (CS332) | Assignment 9
## Distributed State & Service Discovery

This solution provides complete, runnable steps and manifest files for all questions in [Ques.md](Ques.md).

## Folder Structure

- [Ques.md](Ques.md): assignment prompt in markdown format
- [docker/node-id-app](docker/node-id-app): custom Python application for Questions 5 & 6
- [k8s/manifests](k8s/manifests): Kubernetes PV/PVC, ConfigMap, Deployment, and Service manifests
- [docs/OBSERVATIONS.md](docs/OBSERVATIONS.md): notes template to record outputs

---

## Part 0 – Bootstrap (Warm-up Tasks)

### Q1) Environment Variables

Run an Alpine container with an environment variable and print it:

```bash
docker run --rm -e MY_NAME=Student alpine sh -c 'echo "MY_NAME=$MY_NAME"'
```

Expected:
- Output prints `MY_NAME=Student`.
- The `-e` flag injects the variable into that single container's environment.

### Q2) Simple Shared Volume

Create a named volume:

```bash
docker volume create lab9-shared
```

Run a container, mount the volume, create a file:

```bash
docker run --rm -v lab9-shared:/data alpine sh -c 'echo "hello from container-1" > /data/greeting.txt'
```

Run a second container with the same volume and verify:

```bash
docker run --rm -v lab9-shared:/data alpine cat /data/greeting.txt
```

Expected:
- Second container prints `hello from container-1`.
- Data persists across container lifecycles via the named volume.

Cleanup (optional):

```bash
docker volume rm lab9-shared
```

---

## Part A – Persistent Storage

### Q3) Docker Volumes with Redis

Create a volume for Redis data:

```bash
docker volume create redis-data
```

Run Redis with persistence enabled (AOF):

```bash
docker run -d --name lab9-redis -v redis-data:/data redis redis-server --appendonly yes
```

Add data:

```bash
docker exec lab9-redis redis-cli SET course "Distributed Computing"
docker exec lab9-redis redis-cli GET course
```

Delete and recreate the container with the same volume:

```bash
docker rm -f lab9-redis
docker run -d --name lab9-redis -v redis-data:/data redis redis-server --appendonly yes
```

Verify data persists:

```bash
docker exec lab9-redis redis-cli GET course
```

Expected:
- `GET course` returns `"Distributed Computing"` even after container deletion and recreation.
- The `--appendonly yes` flag enables Redis AOF persistence to the `/data` directory.

Cleanup (optional):

```bash
docker rm -f lab9-redis
docker volume rm redis-data
```

### Q4) Kubernetes PVC

Start your Kind cluster:

```bash
kind create cluster --name lab9
```

Create PV and PVC:

```bash
kubectl apply -f k8s/manifests/pv-pvc.yaml
```

Verify binding:

```bash
kubectl get pv,pvc
```

Deploy a pod that mounts the PVC:

```bash
kubectl apply -f k8s/manifests/pvc-pod.yaml
```

Write data inside the pod:

```bash
kubectl exec pvc-test-pod -- sh -c 'echo "persistent data" > /data/test.txt'
kubectl exec pvc-test-pod -- cat /data/test.txt
```

Delete the pod and recreate:

```bash
kubectl delete pod pvc-test-pod
kubectl apply -f k8s/manifests/pvc-pod.yaml
```

Wait for the pod to be ready, then verify data survived:

```bash
kubectl wait --for=condition=Ready pod/pvc-test-pod --timeout=60s
kubectl exec pvc-test-pod -- cat /data/test.txt
```

Expected:
- PV and PVC show `Bound` status.
- After pod deletion and recreation, `/data/test.txt` still contains `persistent data`.

---

## Part B – Environment Variables & ConfigMaps

### Q5) Decoupling Configuration

Build the custom app image and load it into the Kind cluster:

```bash
cd docker/node-id-app
docker build -t lab9-node-id-app:1.0 .
kind load docker-image lab9-node-id-app:1.0 --name lab9
```

Create the ConfigMap and deploy the pod:

```bash
kubectl apply -f k8s/manifests/configmap.yaml
kubectl apply -f k8s/manifests/configmap-pod.yaml
```

Verify the pod reads `NODE_ID`:

```bash
kubectl wait --for=condition=Ready pod/node-id-pod --timeout=60s
kubectl exec node-id-pod -- wget -qO- http://localhost:8000
```

Expected output:
```
NODE_ID  : node-alpha
HOSTNAME : node-id-pod
POD_IP   : <some-ip>
```

Update the ConfigMap:

```bash
kubectl delete pod node-id-pod
kubectl apply -f k8s/manifests/configmap.yaml
```

Before reapplying, edit the ConfigMap to change the value:

```bash
kubectl patch configmap node-config -p '{"data":{"NODE_ID":"node-beta"}}'
```

Recreate the pod and verify change:

```bash
kubectl apply -f k8s/manifests/configmap-pod.yaml
kubectl wait --for=condition=Ready pod/node-id-pod --timeout=60s
kubectl exec node-id-pod -- wget -qO- http://localhost:8000
```

Expected:
- `NODE_ID` now shows `node-beta`.
- Environment variables from ConfigMaps require pod restart to reflect updates.

---

## Part C – Internal Load Balancing

### Q6) Scaling and Service Discovery

Ensure ConfigMap exists (already applied in Q5, or apply now):

```bash
kubectl apply -f k8s/manifests/configmap.yaml
```

Delete the standalone pod from Q5 (if still running):

```bash
kubectl delete pod node-id-pod --ignore-not-found
```

Create the Deployment (3 replicas) and ClusterIP Service:

```bash
kubectl apply -f k8s/manifests/deployment.yaml
kubectl apply -f k8s/manifests/node-id-service.yaml
```

Verify all three replicas are running:

```bash
kubectl get pods -l app=node-id -o wide
```

Deploy a client pod:

```bash
kubectl apply -f k8s/manifests/client-pod.yaml
```

Send multiple requests from the client pod to observe load balancing:

```bash
kubectl wait --for=condition=Ready pod/client-pod --timeout=60s
for i in $(seq 1 6); do
  kubectl exec client-pod -- wget -qO- http://node-id-svc
  echo "---"
done
```

Expected:
- Each request may be served by a different pod (different `HOSTNAME` / `POD_IP`).
- The ClusterIP Service distributes traffic across the 3 replicas using round-robin (or random) selection.

---

## Important Viva Points

1. **Docker Volumes** persist data independently of container lifecycle; named volumes are managed by Docker.
2. **Redis AOF (`--appendonly yes`)** writes every operation to disk, ensuring data survives container restarts.
3. **PersistentVolume (PV)** is cluster-level storage; **PersistentVolumeClaim (PVC)** is a pod's request for storage.
4. **ConfigMaps** decouple configuration from container images; environment variables injected via `envFrom` require pod restart to pick up changes.
5. **ClusterIP Service** provides a stable internal IP and DNS name; `kube-proxy` performs L4 load balancing across pod endpoints.
6. **Service Discovery** in Kubernetes uses CoreDNS — pods resolve service names like `node-id-svc` to the ClusterIP automatically.

---

## Cleanup Commands

### Kubernetes

```bash
kubectl delete -f k8s/manifests/client-pod.yaml --ignore-not-found
kubectl delete -f k8s/manifests/node-id-service.yaml --ignore-not-found
kubectl delete -f k8s/manifests/deployment.yaml --ignore-not-found
kubectl delete -f k8s/manifests/configmap-pod.yaml --ignore-not-found
kubectl delete -f k8s/manifests/configmap.yaml --ignore-not-found
kubectl delete -f k8s/manifests/pvc-pod.yaml --ignore-not-found
kubectl delete -f k8s/manifests/pv-pvc.yaml --ignore-not-found
```

### Docker

```bash
docker rm -f lab9-redis 2>/dev/null
docker volume rm redis-data lab9-shared 2>/dev/null
```

### Kind

```bash
kind delete cluster --name lab9
```

Use [docs/OBSERVATIONS.md](docs/OBSERVATIONS.md) to fill actual outputs/screenshots for submission.
