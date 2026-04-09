from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    log_level: str = "INFO"
    aws_region: str = "us-east-1"
    incident_max_retries: int = 2
    action_mode: str = "simulation"
    incident_memory_backend: str = "local"
    search_backend: str = "local"
    raw_logs_path: str = "./data/artifacts/raw-logs"
    seed_data_path: str = "./data/seed/incidents.json"
    bedrock_model_id: str | None = None
    opensearch_endpoint: str | None = None
    dynamodb_incident_table: str | None = None
    s3_artifact_bucket: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
