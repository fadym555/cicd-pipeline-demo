from fastapi import FastAPI
import os

app = FastAPI(title="cicd-pipeline-demo")


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/version")
def version() -> dict:
    return {"version": os.getenv("APP_VERSION", "dev")}
