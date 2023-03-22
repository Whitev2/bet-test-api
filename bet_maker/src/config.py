from pydantic import BaseSettings, PostgresDsn


class Config(BaseSettings):
    PostgresUrl: PostgresDsn = None

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = None
    ALGORITHM: str = None

    provider_event_url = 'http://bet_provider:8001'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Config()
