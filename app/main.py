
import logging

from fastapi import FastAPI

from app.artifact_loader import ArtifactLoader
from app.config import settings
from app.logging_config import configure_logging
from app.routes import router, set_artifact

configure_logging(settings.log_level)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Artifact Service",
    version="1.0.0"
)

loader = ArtifactLoader(settings.artifact_version)

artifact_data = loader.load()

set_artifact(artifact_data)

logger.info(
    f"Application started with artifact version "
    f"{settings.artifact_version}"
)

app.include_router(router)