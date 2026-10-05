# Docker Core Concepts & Reference Guide

A practical reference guide covering essential Docker concepts, networking, orchestration, registries, and common commands.

---

## Table of Contents
1. [Images](#1-docker-images)
2. [Containers](#2-docker-containers)
3. [Docker Networking & Linking](#3-docker-networking--linking)
4. [Docker Compose](#4-docker-compose)
5. [Docker Registries](#5-docker-registries)
6. [Commands & Multiline Syntax](#6-commands--multiline-syntax)

---

## 1. Docker Images

An **Image** is a read-only template containing the application code, libraries, dependencies, tools, and runtime environment needed to execute an application.

* **Key Characteristics:**
  * **Immutable:** Once built, an image cannot be changed. Updates require creating a new layer or image.
  * **Layered File System:** Images are composed of stacked read-only layers (Union File System). Each command in a `Dockerfile` adds a new layer.
  * **Shared Base:** Multiple images can share lower layers (e.g., base OS layers like `ubuntu` or `alpine`), saving storage and build time.

### Common Image Commands
```bash
# List locally cached images
docker image ls

# Pull an image from Docker Hub
docker pull node:18-alpine

# Remove an image
docker image rm <image_id_or_name>

# Inspect detailed image metadata
docker image inspect <image_name>
```

---

## 2. Docker Containers

A **Container** is a runnable, isolated instance of an Image. It adds a thin **writeable layer** (container layer) on top of the underlying read-only image layers.

* **Key Characteristics:**
  * **Ephemerality:** Data written inside a container layer is deleted when the container is removed (unless persisted using Docker Volumes or Bind Mounts).
  * **Isolation:** Uses Linux Kernel namespaces (PID, NET, IPC) and cgroups (resource limits) to run isolated from other processes on the host.

### Common Container Commands
```bash
# Run a container in detached (background) mode with port mapping
docker run -d -p 8080:80 --name my-web-app nginx

# List running containers
docker ps

# List all containers (including stopped ones)
docker ps -a

# Execute an interactive terminal inside a running container
docker exec -it my-web-app /bin/bash

# Stop and remove a container
docker stop my-web-app
docker rm my-web-app

# Creates a container
docker build -t my-app-name 

# Runs the container 
docker run -d -p 8000:8000 my-app-name
```

---

## 3. Docker Networking & Linking

Docker networking enables containers to communicate with each other and with external networks.

### Built-in Network Drivers
* **`bridge` (Default):** Isolated network space on a single host. Containers attached to the same custom bridge network can communicate using container names as DNS hostnames.
* **`host`:** Removes network isolation between container and host; uses host's network directly.
* **`none`:** Disables all networking for the container.
* **`overlay`:** Enables multi-host networking across multiple Docker daemons (used in Swarm mode).

### Connecting Containers
> ⚠️ **Note on Legacy Linking (`--link`):** The `--link` flag is deprecated. Use **Custom User-Defined Bridge Networks** instead for modern container-to-container communication.

```bash
# 1. Create a custom bridge network
docker network create my-app-net

# 2. Run container A on the network
docker run -d --name db-server --network my-app-net postgres

# 3. Run container B on the same network (it can reach 'db-server' by name)
docker run -d --name web-app --network my-app-net -e DB_HOST=db-server my-web-image
```

---

## 4. Docker Compose

**Docker Compose** is a tool for defining and running multi-container Docker applications using a single `docker-compose.yml` configuration file.

* Automatically handles container creation, networks, volumes, and dependency ordering (`depends_on`).
* Ideal for managing local development environments.

### Example `docker-compose.yml`
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=database
    depends_on:
      - database

  database:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secretpassword
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

### Essential Compose Commands
```bash
# Start all services in detached mode (and build if necessary)
docker compose up -d

# Stop and remove containers, networks, and volumes created by Compose
docker compose down -v

# View logs from all running services
docker compose logs -f
```

---

## 5. Docker Registries

A **Registry** is a hosted service that stores and distributes Docker images.
* **Public Registries:** Docker Hub, GitHub Packages (GHCR), Amazon ECR, Quay.io.
* **Private Registries:** Self-hosted registries or secure cloud-provided instances.

### Image Tagging Strategy
Image names generally follow the pattern: `<registry_host>/<username_or_org>/<repository_name>:<tag>`

### Registry Workflow
```bash
# 1. Log in to a registry
docker login

# 2. Tag a local image for a target repository
docker tag my-local-image:latest myusername/my-web-app:v1.0.0

# 3. Push the image to the registry
docker push myusername/my-web-app:v1.0.0

# 4. Pull the image on another machine
docker pull myusername/my-web-app:v1.0.0
```

---

## 6. Commands & Multiline Syntax

### Multiline Commands in Dockerfile (`\`)
To keep images lightweight, combine multiple shell commands into a single `RUN` instruction using `&&` and line continuations (`\`). This prevents unnecessary layer creation.

```dockerfile
# Efficient multiline Dockerfile layer
RUN apt-get update && apt-get install -y \
    curl \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*
```

### Multiline Commands in Terminal / Scripts
Break long CLI commands into readable lines using `\` in Bash/Zsh:

```bash
docker run -d \
  --name production-api \
  --publish 8080:8080 \
  --network production-net \
  --env NODE_ENV=production \
  --restart unless-stopped \
  my-company/api:v2.1.0
```

### Useful CLI Quick Reference

| Action | Command |
| :--- | :--- |
| Clean unused data (containers, networks, images) | `docker system prune -a` |
| Stream live container resource usage | `docker stats` |
| View container logs | `docker logs -f <container_name>` |
| Copy files between host and container | `docker cp <host_path> <container>:<path>` |