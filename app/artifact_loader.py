
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ArtifactLoader:
    def __init__(self, version: str):
        self.version = version
        self.data = None

    def load(self):
        path = Path(f"artifacts/{self.version}.json")

        logger.info(f"Loading artifact from {path}")

        if not path.exists():
            raise FileNotFoundError(
                f"Artifact not found: {path}"
            )

        try:
            with open(path) as f:
                self.data = json.load(f)

        except json.JSONDecodeError as e:
            logger.error(
                f"Invalid JSON in artifact file {path}: {e}"
            )

            raise RuntimeError(
                f"Artifact file contains invalid JSON: {path}"
            ) from e

        logger.info(
            f"Successfully loaded artifact version "
            f"{self.version}"
        )

        return self.data