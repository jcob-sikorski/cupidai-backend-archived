from functools import lru_cache

from model.auth import Settings

@lru_cache()
def get_settings() -> Settings:
    return Settings()