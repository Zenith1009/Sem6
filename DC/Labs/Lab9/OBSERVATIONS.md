# Lab 9 Observation Notes

This is my working record for Lab 9. I have written each answer in a way that reflects what I actually observed while running the commands.

## Q1 - Environment Variable Check
I launched an Alpine container with the environment variable MY_NAME set to Student.
The container printed the expected value, so this confirmed that the variable was injected correctly for that container run.

## Q2 - Shared Docker Volume
I created a named volume and wrote a file from the first container.
Then I started a second container with the same volume mount and read the same file successfully.
This showed that the data was stored in the volume, not in a single container filesystem.

## Q3 - Redis Persistence with Volume
I ran Redis with a volume mounted at /data and enabled append-only persistence.
After setting a key, I removed the container and started a new one using the same volume.
The key was still present, which confirmed persistence across container recreation.

## Q4 - Kubernetes PVC Persistence
I applied the PV and PVC manifest and checked that the claim was bound.
After writing test data from the pod, I deleted and recreated the pod.
The same file content was still available after recreation, proving PVC-backed persistence.

## Q5 - ConfigMap and Pod Environment
I deployed the app pod using values from the ConfigMap.
The endpoint response showed NODE_ID from the ConfigMap as expected.
After updating NODE_ID in the ConfigMap and recreating the pod, the new value appeared in the app response.
One practical note: if the manifest file still contains node-alpha, applying it again resets the ConfigMap back to node-alpha.

## Q6 - Service Discovery and Internal Load Balancing
I created a Deployment with 3 replicas and exposed it with a ClusterIP Service.
From the client pod, I sent repeated requests to the service DNS name.
Responses came from different backend pods (different HOSTNAME and POD_IP values), which verified internal load balancing.

## Final Reflection
This lab made the difference between container-local state and externalized state very clear.
Volumes and PVCs handled persistence, ConfigMaps handled configuration, and Services handled discovery and traffic distribution.
