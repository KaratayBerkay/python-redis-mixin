from typing import Union, Optional

from controller import RedisController, redis_controller
from schemas import RedisSchema
from rows import RedisRow


class RedisClient:

    __controller: RedisController = None

    def __init__(self, controller: RedisController):
        self.__controller = controller

    def set_schema(self, schema: RedisSchema) -> bool:
        pass

    def find(self, keys: Union[list[str], str]) -> RedisRow:
        pass

    def store(
        self,
        keys: Union[list[str], str],
        value: Union[dict, bytes, list, str],
        expires_at: Optional[dict] = None,
    ) -> RedisRow:
        pass


redis_client = RedisClient(controller=redis_controller)
