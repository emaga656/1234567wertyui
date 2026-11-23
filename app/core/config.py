from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "TaskFlow API"
    environment: str = "development"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60
    database_url: str = "postgresql+psycopg://taskflow:taskflow@localhost:5432/taskflow"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: str = "http://localhost:3000"
    rate_limit_login: str = "5/minute"
    admin_email: str = "admin@example.com"
    admin_password: str = "ChangeMe123!"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

settings = Settings()
