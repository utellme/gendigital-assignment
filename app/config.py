from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    artifact_version: str = "v1"
    log_level: str = "INFO"

    class Config:
        env_prefix = ""
        case_sensitive = False


settings = Settings()