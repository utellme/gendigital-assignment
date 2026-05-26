from app.artifact_loader import ArtifactLoader


def test_artifact_load():
    loader = ArtifactLoader("v1")

    data = loader.load()

    assert data["version"] == "v1"