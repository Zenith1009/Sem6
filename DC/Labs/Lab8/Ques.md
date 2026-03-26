# Distributed Computing
## Assignment 8

## Part A - Docker

### Question 1: Docker Installation
Install Docker on your system and verify the installation.

### Question 2: Running a Simple Container
Run a simple container (for example, `welcome-to-docker` or any basic image).

- Show that the container runs successfully.
- List all running containers.
- List all containers, including stopped containers.

### Question 3: Creating a Custom Docker Image
Create your own Docker image:

1. Create a simple application (any language).
2. Write a Dockerfile.
3. Build the image.
4. Run a container from your image.
5. Access the application from a browser or terminal.

### Question 4: Custom Docker Network and Inter-Container Communication
Create a custom Docker network.

- Run two containers inside this network.
- Test communication between them using the container name.
- Show their IP addresses using an appropriate command.

## Part B - Kubernetes Pods

### Question 5: Single Pod Deployment
Kubernetes installation and testing.

1. Set up your local Kubernetes cluster using either Minikube or Kind.
2. Deploy a single Pod using a YAML file to run a simple container.
3. Verify the Pod status.
4. Display the Pod IP address.

### Question 6: Multiple Pods and IP Comparison
Create multiple Pods (at least 3).

- List their IP addresses.
- Observe whether the IP addresses are the same or different.
- Delete one Pod and recreate it. Compare the IP address before and after recreation.

## Part C - Inter-Pod Communication

### Question 7: Accessing a Pod by IP
Deploy:

- One Pod running a web application.
- One Pod used for testing (for example, busybox).

From the second Pod:

- Access the first Pod using its IP address.
- Show the response.

### Question 8: Service for Pod Access
Create a Service for the web Pod.

- Access the web application using the Service name from the second Pod.
- Compare Service access with direct Pod IP access.
