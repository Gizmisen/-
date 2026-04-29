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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
