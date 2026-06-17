# Kubernetes Enterprise Homelab Platform

A comprehensive, production-grade DevOps and GitOps homelab environment built to simulate modern cloud-native banking infrastructure. This project demonstrates hands-on experience with Linux administration, container orchestration, automated deployments, and observability.

## 🏗️ Architecture Overview
This lab is hosted on a local Linux environment, orchestrating applications using a lightweight Kubernetes distribution, managed via GitOps principles, and monitored with an enterprise-grade observability stack.

*Architecture Diagram coming soon*

## 🛠️ Technology Stack & Skills Demonstrated
- **OS/Infrastructure:** Linux (Ubuntu Server), Virtualization (VMware/VirtualBox)
- **Container Orchestration:** Kubernetes (K3s / Kind)
- **GitOps & CI/CD:** ArgoCD, GitHub
- **Automation & Scripting:** Python, Infrastructure-as-Code (Terraform)
- **Observability:** Prometheus, Grafana

---

## 🚀 Project Roadmap & Progress

### 🖥️ Phase 1: Infrastructure & Linux Foundation
- [x] Setup Linux Virtual Machine (Ubuntu Server)
- [x] Configure SSH, Networking, and Firewall (UFW)
- [x] Install and configure Container Runtime (Docker/Containerd)

### ☸️ Phase 2: Kubernetes Core Setup
- [x] Deploy K3s/Kind Kubernetes Cluster
- [x] Configure Cluster Networking & Ingress Controller (Nginx/Traefik)
- [x] Implement Secret and ConfigMap management

### 🔄 Phase 3: GitOps with ArgoCD
- [ ] Install ArgoCD inside the cluster
- [ ] Connect this GitHub repository to ArgoCD
- [ ] Deploy a sample Python API using GitOps auto-sync

### 📊 Phase 4: Observability & Monitoring
- [ ] Deploy Prometheus and Grafana
- [ ] Create a custom Grafana Dashboard for Cluster Metrics

### 🤖 Phase 5: Python Automation & AI/ML Experimentation
- [ ] Write a Python script using `kubernetes-client` to monitor cluster health
- [ ] Automate self-healing (auto-restart failing pods) or log analysis

---

## 📖 Step-by-Step Implementation Log

### Phase 1: Infrastructure & Linux Foundation

#### 1. Virtual Machine Provisioning
- **Hypervisor:** VMware Workstation
- **OS:** Ubuntu Server 24.04 LTS
- **Specs:** 4 vCPUs, 4GB RAM, 30GB Disk
- **Network IP:** 192.168.95.153

```bash
# Updating and upgrading the system:
sudo apt update && sudo apt upgrade -y
```
<img src="images/1_vmware_specs.png" alt="VMware Specs" width="400">
<img src="images/2_linux_installed.png" alt="Linux Installed" width="700">

#### 2. Firewall & SSH Configuration
To secure the node, the Uncomplicated Firewall (UFW) was enabled, allowing only explicitly permitted traffic, starting with SSH (port 22).

```bash
# Allowing SSH traffic on port 22 through the firewall
sudo ufw allow ssh

# Activating the firewall
sudo ufw enable

# Checking if the firewall is active
sudo ufw status verbose
```

<img src="images/4_ufw_status.png" alt="Firewall status" width="600">

#### 3. Container Runtime Installation (Docker)
To enable container orchestration, Docker was installed and configured as the container runtime interface (CRI). The system user was added to the docker group to allow non-root execution.

```bash
# Installing Docker and configuring group
sudo apt install docker.io -y
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker

# Verifying installation
docker run hello-world
```

<img src="images/5_docker_hello_world.png" alt="Docker Verification" width="600">


### Phase 2: Kubernetes Core Setup

#### 1. K3s Cluster Deployment
A single-node Kubernetes cluster was deployed using K3s. Firewall rules were updated to allow traffic on port 6443 (Kubernetes API server). The kubeconfig file permissions were configured to allow the non-root `ubuntu` user to manage the cluster using kubectl.

- Kubernetes Distribution: K3s v1.35.5+k3s1

```bash
# Opening Kubernetes API port
sudo ufw allow 6443/tcp

# Installing K3s with user access permissions
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644

# Verifying cluster nodes and system pods
kubectl get nodes
kubectl get pods -A
```

<img src="images/6_k3s_cluster_status.png" alt="k3s Cluster Status" width="600">


#### 2. Cluster Networking & Ingress Routing
To route external HTTP traffic into the cluster, firewall ports 80 and 443 were opened. A test deployment using an Nginx web server was deployed alongside a Kubernetes Service and an Ingress resource managed by the built-in Traefik controller.

```bash
# Opening HTTP and HTTPS ports
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Deploying the Nginx application and Ingress rule
kubectl apply -f ingress-test.yaml

# Verifying ingress routing
kubectl get ingress
```

<img src="images/7_ingress_nginx_success.png" alt="Ingress Routing Verification" width="400">


#### 3. Configuration & Secret Management
To demonstrate secure application configuration, a `ConfigMap` was created for non-sensitive environment variables, and a `Secret` resource was implemented for sensitive data (such as database credentials). A test pod was deployed to inject these resources as environment variables, verifying successful decryption and decoupling of configuration from container images.

```bash
# Applying ConfigMap, Secret, and Test Pod
kubectl apply -f k8s-config-test.yaml

# Inspecting container logs to verify environment variable injection
kubectl logs config-test-pod
```

<img src="images/8_k8s_secrets_logs.png" alt="Container logs" width="600">




