from typing import Union, Optional

from controller import RedisController, redis_controller
from schemas import RedisSchema
from rows import MultipleRows, RedisRow


class RedisClient:

    __controller: RedisController = None
    __schema: RedisSchema = None

    def __init__(self, controller: RedisController):
        self.__controller = controller

    def set_schema(self, schema: RedisSchema) -> bool:
        pass

    def check_schema(self) -> bool:
        pass


    def find(self, keys_dict: dict) -> Optional[MultipleRows]:
        """
        Args:
            keys_dict:  {
                "DynamicKey": "KeyToFind",
            }
        Returns:
            Returns a RedisRow object or None
        """
        if not self.__schema:
            raise Exception("Declare schema first. Redis Controller needs a schema to match key patterns.")

        match_key: str = self.__schema.merge_key(key_dict=keys_dict)
        list_of_rows, json_rows = [], self.__controller.read_cli.scan_iter(match=match_key)
        for json_row in list(json_rows):
            redis_row = RedisRow(schema=self.__schema, delimiter=self.__schema.delimiter)
            redis_row.feed(value=json_row)
            list_of_rows.append(redis_row)
        if list_of_rows:
            return MultipleRows(rows=list_of_rows)
        return None

    def store(
        self,
        keys: Union[list[str], str],
        value: Union[dict, bytes, list, str],
        expires_at: Optional[dict] = None,
    ) -> RedisRow:
        """
        Args:
            keys:
            value:
            expires_at: Optional[dict]
            {
                "days": int,
                "hours": int,
                "minutes": int,
                "seconds": int,
            }
        Returns:
            RedisRow object or raises an exception
        """


        pass


redis_client = RedisClient(controller=redis_controller)
