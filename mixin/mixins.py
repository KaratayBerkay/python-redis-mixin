from typing import Union, Optional, Dict
from .controller import RedisController, redis_controller
from .schemas import RedisSchema
from .rows import MultipleRows, RedisRow


class RedisClient:

    __controller: RedisController = None
    __schema: RedisSchema = None

    def __init__(self, controller: RedisController):
        self.__controller = controller

    @classmethod
    def get_expiry_time(cls, expiry_kwargs: Dict[str, int]) -> int:
        """Calculate expiry time in seconds from kwargs."""
        time_multipliers = {"days": 86400, "hours": 3600, "minutes": 60, "seconds": 1}
        return sum(
            int(expiry_kwargs.get(unit, 0)) * multiplier
            for unit, multiplier in time_multipliers.items()
        )

    @classmethod
    def set_expiry_time(cls, expiry_seconds: int) -> Dict[str, int]:
        """Convert total seconds back into a dictionary of time units."""
        time_multipliers = {"days": 86400, "hours": 3600, "minutes": 60, "seconds": 1}
        result = {}
        for unit, multiplier in time_multipliers.items():
            if expiry_seconds >= multiplier:
                result[unit], expiry_seconds = divmod(expiry_seconds, multiplier)
        return result

    def set_schema(self, schema: RedisSchema) -> None:
        """
        Args:
            schema: RedisSchema object to change schema of redis key pattern
        """
        self.__schema = schema

    def check_schema(self) -> None:
        """
        Check if schema is declared. If not raise an exception.
        """
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
        redis_row = RedisRow(schema=self.__schema, delimiter=self.__schema.delimiter)
        redis_row.set_key(key_dict=self.dynamic_key_list_to_dict(dynamic_keys=keys))
        redis_row.feed(value=value)
        if expires_at:
            self.__controller.write_cli.setex(
                name=redis_row.key,
                time=self.get_expiry_time(expiry_kwargs=expires_at),
                value=redis_row.value,
            )
        else:
            self.__controller.write_cli.set(name=redis_row.key, value=redis_row.value)
        return redis_row


redis_client = RedisClient(controller=redis_controller)
