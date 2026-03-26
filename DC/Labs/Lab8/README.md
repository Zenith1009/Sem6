# Distributed Computing (CS332) | Assignment 8
## Docker Containers and Kubernetes Pod Networking

This solution provides complete, runnable steps and manifest files for all questions in [Ques.md](Ques.md).

## Folder Structure

- [Ques.md](Ques.md): assignment prompt in markdown format
- [docker/custom-app](docker/custom-app): custom Docker application for Question 3
- [k8s/manifests](k8s/manifests): Kubernetes Pod and Service manifests for Questions 5-8
- [docs/OBSERVATIONS.md](docs/OBSERVATIONS.md): notes template to record outputs

---

## Part A - Docker

### Q1) Docker Installation and Verification

Run:

```bash
docker --version
docker info
```

Expected:
- Docker CLI version should print.
- Docker daemon info should print without connection errors.

### Q2) Run a Simple Container + Listing Containers

Run a basic image:

```bash
docker run --name q2-hello hello-world
```

List running containers:

```bash
docker ps
```

List all containers including stopped:

```bash
docker ps -a
```

Expected:
- `hello-world` container runs and exits after printing success message.
- `docker ps` may show none running (because hello-world exits).
- `docker ps -a` shows `q2-hello` with `Exited` state.

### Q3) Create and Run Custom Docker Image

Files used:
- [docker/custom-app/app.py](docker/custom-app/app.py)
- [docker/custom-app/Dockerfile](docker/custom-app/Dockerfile)

Build image:

```bash
cd docker/custom-app
docker build -t lab8-custom-app:1.0 .
```

Run container:

```bash
docker run -d --name lab8-custom-app -p 8000:8000 lab8-custom-app:1.0
```

Access application:

```bash
curl http://localhost:8000
```

Expected response contains:
- `Lab 8 Custom Docker App is running.`

Stop and remove container (optional):

```bash
docker stop lab8-custom-app
docker rm lab8-custom-app
```

### Q4) Custom Docker Network and Inter-Container Communication

Create custom network:

```bash
docker network create lab8-net
```

Run two containers in this network:

```bash
docker run -d --name netbox1 --network lab8-net alpine sleep 3600
docker run -d --name netbox2 --network lab8-net alpine sleep 3600
```

Test name-based communication from `netbox1` to `netbox2`:

```bash
docker exec netbox1 ping -c 3 netbox2
```

Show container IP addresses:

```bash
docker inspect -f '{{.Name}} -> {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' netbox1 netbox2
```

Expected:
- `ping` resolves `netbox2` by container name.
- Both containers have different IPs in subnet of `lab8-net`.

Cleanup (optional):

```bash
docker rm -f netbox1 netbox2
docker network rm lab8-net
```

---

## Part B - Kubernetes Pods

You can use either Minikube or Kind.

### Option A: Minikube quick start

```bash
minikube start
kubectl cluster-info
```

### Option B: Kind quick start

```bash
kind create cluster --name lab8
kubectl cluster-info
```

### Q5) Single Pod Deployment + Pod IP

Apply manifest:

```bash
kubectl apply -f k8s/manifests/single-pod.yaml
```

Check status:

```bash
kubectl get pod single-nginx-pod
kubectl get pod single-nginx-pod -o wide
```

Expected:
- Status becomes `Running`.
- Pod IP appears in `-o wide` output.

### Q6) Multiple Pods + IP Comparison + Recreate

Apply three pods:

```bash
kubectl apply -f k8s/manifests/multi-pods.yaml
```

List pod IPs:

```bash
kubectl get pods -l group=multi-demo -o wide
```

Delete one pod and recreate:

```bash
kubectl get pod pod-b -o wide
kubectl delete pod pod-b
kubectl apply -f k8s/manifests/multi-pods.yaml
kubectl get pod pod-b -o wide
```

Expected:
- `pod-a`, `pod-b`, `pod-c` usually have different IPs.
- Recreated `pod-b` may get a different IP than before.

---

## Part C - Inter-Pod Communication

### Q7) Access Web Pod by Direct Pod IP

Apply web pod and tester pod:

```bash
kubectl apply -f k8s/manifests/web-pod.yaml
kubectl apply -f k8s/manifests/tester-pod.yaml
```

Get web pod IP:

```bash
WEB_IP=$(kubectl get pod web-pod -o jsonpath='{.status.podIP}')
echo "$WEB_IP"
```

Access web pod from tester pod:

```bash
kubectl exec tester-pod -- wget -qO- "http://$WEB_IP"
```

Expected:
- HTML response from nginx default page.

### Q8) Access Web Pod through Service Name

Create service:

```bash
kubectl apply -f k8s/manifests/web-service.yaml
```

Access through service DNS from tester pod:

```bash
kubectl exec tester-pod -- wget -qO- http://web-svc
```

Compare with direct Pod IP:

- Direct Pod IP is tied to pod lifecycle (can change on recreate).
- Service name (`web-svc`) stays stable and routes to matching pods.

---

## Important Viva Points

1. Docker network provides container-level DNS by container name.
2. Pod IPs are ephemeral; recreating pod may change IP.
3. Kubernetes Service provides stable virtual endpoint independent of Pod IP changes.
4. Inter-pod communication works directly by Pod IP, but Service is preferred for reliability.

---

## Cleanup Commands

### Kubernetes

```bash
kubectl delete -f k8s/manifests/web-service.yaml --ignore-not-found
kubectl delete -f k8s/manifests/tester-pod.yaml --ignore-not-found
kubectl delete -f k8s/manifests/web-pod.yaml --ignore-not-found
kubectl delete -f k8s/manifests/multi-pods.yaml --ignore-not-found
kubectl delete -f k8s/manifests/single-pod.yaml --ignore-not-found
```

### Kind (if used)

```bash
kind delete cluster --name lab8
```

### Minikube (if used)

```bash
minikube stop
```

Use [docs/OBSERVATIONS.md](docs/OBSERVATIONS.md) to fill actual outputs/screenshots for submission.
