### What is a Docker Registry?

A **Docker Registry** is a centralized storage and distribution system for Docker container images. It allows you to store, share, and manage images privately or publicly. Think of it as a "GitHub for Docker images."

- **Repository**: A collection of related images (often versions with different tags, like `latest`, `v1.0`).
- **Default Registry**: Docker Hub (hub.docker.com) – public and free for basic use.
- **Alternatives**: Private/self-hosted (using the open-source `registry` image), cloud-based like AWS ECR, Azure ACR, Google Artifact Registry, or enterprise tools like Harbor.












### Key Docker Registry Commands

These are the most common CLI commands for working with registries (primarily Docker Hub or private ones).

| Command                  | Description                                                                 | Example Usage                                                                 |
|--------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| `docker login`          | Authenticate to a registry (prompts for username/password or token). Default: Docker Hub. | `docker login` <br> `docker login myregistry.com`                             |
| `docker logout`         | Log out from a registry.                                                    | `docker logout` <br> `docker logout myregistry.com`                           |
| `docker pull`           | Download (pull) an image from a registry.                                   | `docker pull nginx:latest` <br> `docker pull myregistry.com/myapp:v1`         |
| `docker tag`            | Tag a local image for pushing to a registry.                                | `docker tag myapp:latest username/myapp:latest` <br> `docker tag myapp localhost:5000/myapp` |
| `docker push`           | Upload (push) a tagged image to a registry.                                 | `docker push username/myapp:latest` <br> `docker push localhost:5000/myapp`   |
| `docker search`         | Search Docker Hub for public images.                                        | `docker search nginx`                                                         |












### Typical Workflow: Push an Image to Docker Hub

1. Build your image: `docker build -t myapp:latest .`
2. Tag it for Docker Hub: `docker tag myapp:latest yourusername/myapp:latest`
3. Login: `docker login`
4. Push: `docker push yourusername/myapp:latest`

### Running a Local/Private Registry (Quick Start)

For testing or private use:

```bash
docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

Then tag and push locally:

```bash
docker tag myapp:latest localhost:5000/myapp:latest
docker push localhost:5000/myapp:latest
docker pull localhost:5000/myapp:latest
```








### Tips
- Always use specific tags (not just `latest`) in production.
- For private registries, configure insecure access if no HTTPS (not recommended for prod).
- Rate limits on Docker Hub: Authenticated users get higher limits.
