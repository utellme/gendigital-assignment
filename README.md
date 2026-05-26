
# Artifact Service

Production-oriented Python microservice demonstrating deployment and operational practices in Kubernetes.

# Overview

This service loads a versioned artifact at startup and exposes it via a REST API.

The goal of this exercise is not complex business logic, but demonstrating:

- clean software design
- operational readiness
- Kubernetes deployment practices
- observability
- CI/CD integration
- rollback and deployment strategy

The service is intentionally lightweight and production-focused.

# Features

- FastAPI-based HTTP service
- Versioned artifact loading
- Structured JSON logging
- Health and readiness probes
- Prometheus metrics endpoint
- Docker containerization
- Kubernetes manifests
- CI pipeline with GitHub Actions
- Horizontal Pod Autoscaler
- Production-oriented security settings

# Repository Structure

```text
.
├── app/
    ├── __init__.py
    ├── main.py
    ├── routes.py
    ├── config.py
    ├── models.py
    ├── logging_config.py
    └── artifact_loader.py
│
├── artifacts/
│   ├── v1.json
│   └── v2.json
│
├── tests/
│   ├── test_api.py
│   ├── test_health.py
│   ├── test_metrics.py
│   ├── test_readiness.py
│   └── test_artifact_loader.py
│
├── k8s/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
│
├── .github/
│   └── workflows/
│       └── ci.yaml
│
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

# Service Behavior

At startup, the application:

1. Reads the configured artifact version
2. Loads the artifact from disk
3. Validates the artifact structure
4. Stores artifact data in memory
5. Exposes APIs for retrieval and operational monitoring

Artifacts simulate versioned ML models or runtime configuration assets.

# API Endpoints

| Endpoint | Purpose |
|---|---|
| `/healthz` | Liveness probe |
| `/readyz` | Readiness probe |
| `/artifact` | Returns loaded artifact |
| `/metrics` | Prometheus metrics |

# Example Artifact

```json
{ "version": "v1",
  "model_name": "model_v1",
  "features": ["a", "b", "c"]
}
```

# Running Locally

# Prerequisites

- Python 3.12+
- Docker
- kind or minikube
- kubectl

# Local Python Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run service:

```bash
uvicorn app.main:app --reload --port 8080
```

Test:

```bash
curl http://localhost:8080/artifact
```

# Run with Docker

Build image:

```bash
docker build -t artifact-service .
```

Run container:

```bash
docker run \
  -p 8080:8080 \
  -e ARTIFACT_VERSION=v1 \
  artifact-service
```

Test:

```bash
curl http://localhost:8080/healthz
```

---

# Run with Docker Compose

Docker Compose is included for local developer ergonomics and reproducible environments.

Start service:

```bash
docker compose up --build
```

Stop service:

```bash
docker compose down
```

# Running in Kubernetes

# Create Cluster

Using kind:

```bash
kind create cluster
```

# Build Docker Image

```bash
docker build -t artifact-service .
```

Load image into kind:

```bash
kind load docker-image artifact-service
```

# Create Namespace
kubectl apply -f k8s/namespace.yaml

Verify:
kubectl get namespaces # verify namespace

# Deploy Application

```bash
kubectl apply -f k8s/
```

Verify:

```bash
kubectl get pods -n artifact-service
```

# Port Forward

```bash
kubectl port-forward \
  -n artifact-service \
  svc/artifact-service \
  8080:80
```

Test:

```bash
curl http://localhost:8080/artifact
```

# Running Tests

Run unit tests:

```bash
pytest -v
```

---

# CI Pipeline

GitHub Actions pipeline performs:

- dependency installation
- unit tests
- Docker image build

Pipeline definition:

```text
.github/workflows/ci.yaml
```

# Design Decisions

# Why FastAPI?

FastAPI was selected because it provides:

- lightweight framework footprint
- strong typing support
- automatic validation
- production-ready ASGI performance
- simple observability integration

The framework keeps focus on infrastructure and operational concerns rather than web framework complexity.


# Why Versioned Artifacts?

Artifacts are treated similarly to ML models or runtime assets.

Separating artifact versioning from application versioning enables:

- independent rollback
- safer deployments
- operational flexibility
- model lifecycle management

Example:

- application version remains stable
- artifact switches from `v2` back to `v1`

without rebuilding the container.


# Why ConfigMaps?

Configuration is externalized through Kubernetes ConfigMaps to separate:

- runtime configuration
- deployment configuration
- application code

This enables:

- environment-specific configuration
- safer promotion across environments
- artifact switching without image rebuild


# Why Readiness and Liveness Probes?

## Readiness Probe

Ensures traffic is only routed after:

- startup completes
- artifact loads successfully

This prevents serving requests during initialization.

## Liveness Probe

Detects unhealthy containers and enables automatic restart behavior.


# Deployment Strategy

The Deployment uses rolling updates:

```yaml
strategy:
  type: RollingUpdate
```

This minimizes downtime during deployments.

Configuration:

- `maxUnavailable: 0`
- `maxSurge: 1`

ensures capacity is maintained during rollout.


# Rollback Strategy

# Kubernetes Rollback

Rollback deployment:

```bash
kubectl rollout undo deployment/artifact-service \
  -n artifact-service
```

# Artifact Rollback

Rollback artifact independently:

Update ConfigMap:

```yaml
ARTIFACT_VERSION=v1
```

then restart deployment:

```bash
kubectl rollout restart deployment/artifact-service \
  -n artifact-service
```

This separation between code deployment and artifact deployment mirrors common ML platform operational patterns.

---

# Operational Notes

---

# Observability

The service exposes:

- health endpoint
- readiness endpoint

Metrics endpoint:

```text
/metrics
```



# Logging

Application logs are written to stdout/stderr following container best practices.
This enables integration with ELS, Datadog, Cloudwatch and others.



# Scaling

Horizontal Pod Autoscaler is included:

```text
k8s/hpa.yaml
```

The HPA scales based on CPU utilization.


# Ingress

Ingress resource is included for HTTP routing.

For local testing:

```text
artifact.local
```

may be mapped in `/etc/hosts`.

---

# Failure Handling

The application intentionally fails fast when:

- artifact files are missing
- artifact parsing fails

This prevents partially initialized containers from serving traffic.

---

# Security Considerations

The deployment includes several production-oriented security settings:

- non-root container
- read-only root filesystem
- disabled privilege escalation
- minimal container image

Additional improvements for production environments could include:

- image vulnerability scanning
- Kubernetes NetworkPolicies
- secrets management
- admission controls
- signed container images


# Tradeoffs

# Simplicity vs Completeness

The implementation intentionally prioritizes:

- readability
- operational clarity
- maintainability

over feature richness.

Business logic is intentionally minimal because the exercise focuses on production engineering practices.


# Useful Commands

---

# View Logs

```bash
kubectl logs deployment/artifact-service \
  -n artifact-service
```

# Describe Deployment

```bash
kubectl describe deployment artifact-service \
  -n artifact-service
```

# Check Rollout Status

```bash
kubectl rollout status deployment/artifact-service \
  -n artifact-service
```

# Delete Deployment

```bash
kubectl delete namespace artifact-service
```