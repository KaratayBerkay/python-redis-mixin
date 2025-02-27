from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Configs(BaseSettings):
    """Base class for all configurations."""

    HOST: str = "localhost"
    PASSWORD: str = ""
    PORT: int = 6379
    DB: int = 0

    REP_1_HOST: str = "localhost"
    REP_1_PASSWORD: str = ""
    REP_1_PORT: int = 6380
    REP_1_DB: int = 0

    REP_2_HOST: str = "localhost"
    REP_2_PASSWORD: str = ""
    REP_2_PORT: int = 6381
    REP_2_DB: int = 0

    model_config = SettingsConfigDict(env_prefix='REDIS_', env_file="../.env")

    @property
    def master_redis_url(self):
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"

    @property
    def first_replica_url(self):
        return f"redis://{self.REP_1_HOST}:{self.REP_1_PORT}/{self.REP_1_DB}"

    @property
    def second_replica_url(self):
        return f"redis://{self.REP_2_HOST}:{self.REP_2_PORT}/{self.REP_2_DB}"


redis_configs = Configs()
