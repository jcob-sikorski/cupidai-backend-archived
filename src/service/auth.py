import data.auth as data

from model.auth import Settings

def get_settings() -> Settings:
    return data.get_settings()