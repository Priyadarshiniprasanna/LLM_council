"""
Application settings loaded from environment variables.

All env vars used anywhere in the app must be declared here.
Add new vars to .env.example at the same time.
"""

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ───────────────────────────────────────────
    app_env: str = "development"
    app_debug: bool = False
    secret_key: str = Field(..., min_length=32)

    # ── Database ──────────────────────────────────────────────
    database_url: str
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # ── Redis ─────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ── Temporal ──────────────────────────────────────────────
    temporal_host: str = "localhost:7233"
    temporal_namespace: str = "default"
    temporal_task_queue: str = "arinar-debate"

    # ── OpenRouter ────────────────────────────────────────────
    openrouter_api_key: str = ""
    openrouter_base_url: AnyHttpUrl = AnyHttpUrl("https://openrouter.ai/api/v1")

    # ── Auth ──────────────────────────────────────────────────
    workos_api_key: str = ""
    workos_client_id: str = ""
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # ── Object Storage ────────────────────────────────────────
    s3_endpoint_url: str = "http://localhost:9000"
    s3_bucket_name: str = "arinar-documents"
    s3_access_key_id: str = ""
    s3_secret_access_key: str = ""

    # ── Observability ─────────────────────────────────────────
    sentry_dsn: str = ""
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"

    # ── Research Gateway ─────────────────────────────────────
    research_gateway_enabled: bool = False
    research_max_requests_per_session: int = 10

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


settings = Settings()  # type: ignore[call-arg]
