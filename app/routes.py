from fastapi import APIRouter
from starlette.responses import Response
from prometheus_client import Counter, generate_latest

from app.models import (
    ArtifactModel,
    HealthResponse,
    ReadinessResponse,
)

router = APIRouter()

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

artifact_data = {}


def set_artifact(data):
    global artifact_data
    artifact_data = data


@router.get("/healthz", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@router.get("/readyz", response_model=ReadinessResponse)
def readiness():
    return {"ready": artifact_data is not None}


@router.get("/artifact", response_model=ArtifactModel)
def artifact():
    REQUEST_COUNT.inc()
    return artifact_data


@router.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )