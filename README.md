# cicd-pipeline-demo

[![CI/CD](https://github.com/fadym555/cicd-pipeline-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/fadym555/cicd-pipeline-demo/actions/workflows/ci.yml)

A small FastAPI service with the kind of delivery pipeline I set up for clients. The app is tiny on purpose. The pipeline is the point: every change is linted, tested, scanned, built into a signed image, deployed to a real Kubernetes cluster and only promoted to production after a human approves it.

## Pipeline

| Stage | What it does |
|---|---|
| **Secret scan** | gitleaks over the whole repo, so credentials never land in git |
| **Lint** | ruff for Python, hadolint for the Dockerfile, `helm lint` for the chart |
| **Test** | pytest on Python 3.11 and 3.12 in parallel, fails under 90% coverage, coverage reports kept as artifacts |
| **Vulnerability & misconfig scan** | Trivy over dependencies, Dockerfile and chart. Results go to the repo's Security tab |
| **Build, scan & SBOM** | Builds the image with layer caching, smoke-tests the container, fails on critical CVEs, publishes an SPDX SBOM |
| **Publish & sign** | Pushes to GHCR and signs the image with cosign (keyless, GitHub OIDC). No signing keys to manage |
| **Deploy to staging** | Spins up a Kubernetes cluster, deploys the signed image with Helm and runs `helm test` |
| **Release to production** | Waits for a reviewer to approve, verifies the signature, then promotes the image to `stable` |

Pull requests run everything up to the build. Only `main` publishes and deploys.

## Verify an image yourself

```bash
cosign verify ghcr.io/fadym555/cicd-pipeline-demo:stable \
  --certificate-identity-regexp '^https://github.com/fadym555/cicd-pipeline-demo/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

## Run it locally

```bash
pip install -r requirements-dev.txt
pytest -v --cov=app
uvicorn app.main:app --reload
```

Or with Docker:

```bash
docker build -t cicd-pipeline-demo .
docker run -p 8000:8000 cicd-pipeline-demo
curl localhost:8000/healthz
```

## Adapting it

The same structure works for Node, Go, Java or .NET. Swap the lint and test steps and keep the rest. Staging can point at any cluster (AKS, EKS, GKE) by replacing the kind step with your cluster credentials.
