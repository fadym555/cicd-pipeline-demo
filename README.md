# cicd-pipeline-demo

[![CI/CD](https://github.com/fadym555/cicd-pipeline-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/fadym555/cicd-pipeline-demo/actions/workflows/ci.yml)

A small FastAPI service I use to show how I set up CI/CD for client projects. The app itself is tiny on purpose. The interesting part is the pipeline.

## What happens on every push

| Stage | What it does |
|---|---|
| **Lint** | `ruff check` so style problems never reach review |
| **Test** | `pytest` on Python 3.11 and 3.12 in parallel, with pip caching |
| **Build & scan** | Builds the Docker image with layer caching, starts the container and hits `/healthz`, then runs Trivy and fails on critical CVEs |
| **Publish** | On `main` only, pushes the image to GHCR tagged with the commit SHA and `latest` |

Pull requests run everything except publishing. A newer push cancels an older run on the same branch, so runners aren't wasted.

## Run it locally

```bash
pip install -r requirements-dev.txt
pytest -v
uvicorn app.main:app --reload
```

Or with Docker:

```bash
docker build -t cicd-pipeline-demo .
docker run -p 8000:8000 cicd-pipeline-demo
curl localhost:8000/healthz
```

Or pull the published image:

```bash
docker pull ghcr.io/fadym555/cicd-pipeline-demo:latest
```

## Endpoints

- `GET /healthz` returns `{"status": "ok"}`
- `GET /version` returns the `APP_VERSION` env var (defaults to `dev`)

## Adapting it

The same structure works for Node, Go or Java. Swap the lint and test steps and keep the build, scan and publish stages. Deploying to Kubernetes, ECS or a VM is one more job after `publish`.
