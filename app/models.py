from pydantic import BaseModel
from typing import List


class ArtifactModel(BaseModel):
    version: str
    model_name: str
    features: List[str]


class HealthResponse(BaseModel):
    status: str


class ReadinessResponse(BaseModel):
    ready: bool