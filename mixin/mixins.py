import arrow

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

    def check_schema(self) -> None:
        if not self.__schema:
            raise Exception("Declare schema first. Redis Controller needs a schema to match key patterns.")

    def find(self, keys_dict: dict) -> Optional[MultipleRows]:
        """
        Args:
            keys_dict:  {
                "DynamicKey": "KeyToFind",
            }
        Returns:
            Returns a RedisRow object or None
        """

        self.check_schema()
        match_key: str = self.__schema.merge_key(key_dict=keys_dict)
        list_of_rows, json_rows = [], self.__controller.read_cli.scan_iter(match=match_key)
        for json_row in list(json_rows):
            redis_row = RedisRow(schema=self.__schema, delimiter=self.__schema.delimiter)
            redis_row.feed(value=json_row)
            list_of_rows.append(redis_row)
        if list_of_rows:
            return MultipleRows(rows=list_of_rows)
        return None

    def dynamic_key_list_to_dict(self, dynamic_keys: list[str]) -> dict:
        """
        Args:
            dynamic_keys: List of dynamic keys
        Returns:
            Dictionary of dynamic keys
        """
        self.check_schema()
        if len(dynamic_keys) != len(self.__schema.dynamics):
            raise Exception("Number of dynamic keys does not match schema.")
        return {self.__schema.dynamics[ix]: dynamic_keys[ix] for ix, _ in enumerate(self.__schema.dynamics)}

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
        self.check_schema()
        redis_row = RedisRow(
            schema=self.__schema, delimiter=self.__schema.delimiter,
        )
        dyn_dict = self.dynamic_key_list_to_dict(dynamic_keys=keys)
        redis_row.set_key(key_dict=dyn_dict)
        redis_row.feed(value=value)
        if expires_at:
            self.__controller.write_cli.setex(
                name=redis_row.key,
                time=100,
                value=redis_row.value,
            )
        else:
            self.__controller.write_cli.set(name=redis_row.key, value=redis_row.value)
        return redis_row


redis_client = RedisClient(controller=redis_controller)
