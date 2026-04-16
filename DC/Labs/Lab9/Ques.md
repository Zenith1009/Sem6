# Distributed Computing
## Assignment 9

## Distributed State & Service Discovery

### Objective
Transition from local container storage to cluster-level configuration and persistence.

## Part 0 – Bootstrap (Warm-up Tasks)

### Question 1: Environment Variables
Run a container with an environment variable (e.g., `docker run -e MY_NAME=Student ...`) and print its value inside the container.

> **Note:** Docker's `-e` flag sets environment variables locally (per container), whereas a ConfigMap defines environment variables at the cluster level.

### Question 2: Simple Shared Volume
Run a container with a volume, create a file, stop the container, start another container using the same volume, and verify that the file persists.

## Part A – Persistent Storage

### Question 3: Docker Volumes with Redis
Run a database container (Redis recommended) with a mounted volume. Add data, delete the container, recreate it using the same volume, and verify that the data persists (ensure Redis persistence is enabled).

### Question 4: Kubernetes PVC
Create a PersistentVolume (PV) and a PersistentVolumeClaim (PVC). Attach them to a Pod and verify that the data survives Pod deletion and recreation using the same PVC.

## Part B – Environment Variables & ConfigMaps

### Question 5: Decoupling Configuration
Create an application that reads `NODE_ID` from an environment variable. Deploy it using a ConfigMap. Update the ConfigMap and observe the behavior change (after restarting or redeploying the Pod).

## Part C – Internal Load Balancing

### Question 6: Scaling and Service Discovery
Create a Deployment with 3 replicas. Expose it via a ClusterIP Service. From a client Pod, send multiple requests. The application must return its `HOSTNAME` or Pod IP to visualize load balancing.

## Helpful Links

- Docker Volumes: https://docs.docker.com/storage/volumes/
- Kubernetes Persistent Volumes: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- Kubernetes ConfigMaps: https://kubernetes.io/docs/concepts/configuration/configmap/
