from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./trustcheck.db"
    port: int = 8000
    environment: str = "development"  # "development" | "production"

    # Scoring — kept here so tuning on Day 4 never touches pipeline code
    signal_weights: dict[str, int] = {
        "URGENT_LANGUAGE": 10,
        "UNREALISTIC_REWARD": 30,
        "SENSITIVE_INFORMATION_REQUEST": 25,
        "PAYMENT_REQUEST": 20,
        "SUSPICIOUS_DOMAIN": 25,
        "BRAND_DOMAIN_MISMATCH": 30,
    }
    risk_thresholds: tuple[tuple[int, str], ...] = (
        (60, "HIGH"),
        (30, "SUSPICIOUS"),
        (0, "LOW"),
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()