# FastAPI + PostgreSQL on Kubernetes

This project demonstrates a scalable FastAPI backend integrated with a PostgreSQL database, deployed using Kubernetes and Kustomize.

## Project Architecture

### 1. Database Connectivity & Service Discovery
The FastAPI backend is configured to connect to the PostgreSQL database using a Kubernetes **Service**.

* **Decoupled Networking:** The three backend replicas do not need to know the specific IP address of the database Pod.
* **Service Discovery:** We utilize a ClusterIP Service named `postgres-service`. Kubernetes provides an internal DNS entry that routes all traffic from the FastAPI pods to the database automatically.
* **Resilience:** If the database Pod is rescheduled or restarted, the Service remains constant, ensuring the backend never loses the connection path.

### 2. Scalability
The backend is configured with `replicas: 3`, providing high availability and load balancing across the application layer.

### 3. Security
* **Environment Secrets:** Database credentials and the connection string are managed via Kubernetes **Secrets**, injected at runtime.
* **Non-Root Execution:** The FastAPI containers are configured to run as non-root users (UID 10001) to follow security best practices.

## How to Deploy

1. Ensure your credentials are set in `db-creds.env`.
2. Apply the configuration using Kustomize:
   ```bash
   kubectl apply -k .

## Lessons Learned & Debugging
I will not talk about my issues when debugging the app and my doker files.I will focus on the K8s part:

### 1. Label Selector Matching
One point of failure was the connection between the **Deployment** and its **Pods**. `matchLabels` and `labels` must match
If these don't match, the Deployment controller cannot "find" the pods it is supposed to manage, and the rollout will hang.

### 2. Service-to-Pod Discovery
The **Service** acts as a bridge. 
The `spec.selector` in the Service must match the labels on your database Pods. 
If the Service selector is wrong, the Service will have no "Endpoints," and the FastAPI app will receive a `Connection Refused` or `DNS Lookup Failure` error.

### 3. DNS and Service Naming
The name of the Service (`metadata.name`) becomes the **hostname** for the database.
In our `.env`, the `POSTGRES_HOST` (or the host part of the `DATABASE_URL`) must match the Service name (`postgres-service`). I fixed an issue where the app was looking for `localhost`, which does not work across different Pods.
