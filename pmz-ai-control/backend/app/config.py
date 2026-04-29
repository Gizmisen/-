from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PMZ AI Control"
    app_env: str = "dev"
    debug: bool = True

    database_url: str = "postgresql+psycopg://pmz:pmz@db:5432/pmz"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    upload_dir: str = "/app/storage/uploads"
    processed_dir: str = "/app/storage/processed"
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"
    instance_name: str = "pmz-main"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

if settings.app_env.lower() in {"prod", "production"}:
    if settings.jwt_secret_key in {"change-me", "CHANGE_ME_TO_STRONG_SECRET"}:
        raise RuntimeError("JWT_SECRET_KEY is insecure for production. Set a strong secret in environment.")
    if settings.allowed_origins.strip() in {"*", ""}:
        raise RuntimeError("ALLOWED_ORIGINS must be explicit in production.")
