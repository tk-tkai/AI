from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "AI Trading Platform"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = Field(default="production")

    API_V1_PREFIX: str = "/api"

    SUPABASE_URL: str
    SUPABASE_KEY: str

    GROQ_API_KEY: str

    BINANCE_BASE_URL: str = "https://api.binance.com"

    INITIAL_PAPER_BALANCE: float = 10000.0

    MARKET_FETCH_INTERVAL_MINUTES: int = 15
    NEWS_FETCH_INTERVAL_MINUTES: int = 30
    SIGNAL_GENERATION_INTERVAL_MINUTES: int = 15
    POSITION_MONITOR_INTERVAL_SECONDS: int = 60

    DEFAULT_TIMEFRAME: str = "15m"

    LOG_LEVEL: str = "INFO"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()