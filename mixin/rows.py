"""
Redis Rows
Redis key-value operations with structured data handling.

This module provides a class for managing Redis key-value operations with support for:
    - Structured data storage and retrieval
    - Key pattern generation for searches
    - JSON serialization/deserialization
    - Type-safe value handling
"""

import json

from typing import Union, Dict, List, Optional, Any
from .errors import RedisKeyError, RedisValueError
from .schemas import RedisSchema


class RedisRow:
    """
    Handles Redis key-value operations with structured data.

    This class provides methods for:
    - Managing compound keys with delimiters
    - Converting between bytes and string formats
    - JSON serialization/deserialization of values
    - Pattern generation for Redis key searches

    Attributes:
        __key: The Redis key in bytes or string format
        __value: The stored value (will be JSON serialized)
        __expires_at: Optional expiration timestamp
    """

    __schema: RedisSchema
    __key: bytes
    __value: str
    __delimiter: str = ":"
    __expires_at: Optional[dict] = {"seconds": 60 * 60 * 30}

    def __init__(self, schema: RedisSchema, delimiter: str = ":"):
        """
        Initialize RedisRow with a static key/keys.
        Args:
            schema: Schema for Redis key which includes static and dynamic keys
            delimiter: Delimiter for compound keys
        """
        self.__schema = schema
        self.__delimiter = delimiter

    @property
    def value(self) -> str:
        """
        Get stored value in JSON format.

        Returns:
            str: JSON serialized data
        """
        return self.__value

    @property
    def data(self) -> Union[Dict, List]:
        """
        Get stored value as Python object.

        Returns:
            Union[Dict, List]: Deserialized JSON data
        """
        try:
            return json.loads(self.__value)
        except json.JSONDecodeError as e:
            raise RedisValueError(f"Invalid JSON format in stored value: {str(e)}")

    # @property
    # def expires_at(self):
    #     """
    #     Get expiration timestamp in string format.
    #     Returns:
    #
    #     """
    #     return arrow.get(self.__expires_at).format("YYYY-MM-DD HH:mm:ss")

    @property
    def as_dict(self) -> Dict[str, Any]:
        """
        Get row data as dictionary.

        Returns:
            Dict[str, Any]: Dictionary with keys and value
        """
        return {"keys": self.key, "value": self.data}

    def clean_key_dict_input(self, key_dict: dict) -> dict:
        """
        Clean key_dict input by removing unnecessary keys.
        Args:
            key_dict: Dictionary of keys
        Returns:
            dict: Cleaned dictionary
        """
        dynamic_key_dict = {}
        for key_dyn in key_dict.keys():  # Remove all items that are not included in schema
            if str(key_dyn).upper() in list(
                str(k).upper() for k in self.__schema.dynamics
            ):
                if str(self.__delimiter) in str(key_dict[key_dyn]):
                    raise RedisKeyError(
                        f"Key value cannot contain delimiter: {self.__delimiter}"
                    )
                dynamic_key_dict[str(key_dyn).upper()] = key_dict[key_dyn]
        return dynamic_key_dict

    def update_key(self, key_dict: dict) -> None:
        """
        Set key by combining static and dynamic keys.
        Args:
            key_dict: {}
                key_name (str): Redis key name
                key_value (str): Redis key value
            {
                "Name": John
            }
            dynamic = [Name, location, UUID]
            dynamic = aaaa:bbbb:cccc
        """
        already_dyn_dict = {}
        already_dyn_keys = list(set(self.key.split(":")) - set(self.__schema.statics))
        if not len(already_dyn_keys) == len(self.__schema.dynamics):
            message = "|".join(self.__schema.dynamics)
            raise RedisKeyError(
                f"Redis Dynamic Key must set before updating key/keys: {message}"
            )

        for ix, already_dyn_key in enumerate(self.__schema.dynamics):
            already_dyn_dict[already_dyn_key] = already_dyn_keys[ix]

        dynamic_key_dict, dynamic_key = self.clean_key_dict_input(key_dict), ""
        upper_dynamic_keys = [str(k).upper() for k in dynamic_key_dict.keys()]
        for upper_dynamic_key in upper_dynamic_keys:
            key_to_set = already_dyn_dict[upper_dynamic_key]
            if upper_dynamic_key in key_dict:
                key_to_set = key_dict[upper_dynamic_key]
            dynamic_key += f"{key_to_set}{self.__delimiter}"
        self.__key = str(dynamic_key[:-1]).encode()

    def set_key(self, key_dict: dict) -> None:
        """
        Set key by combining static and dynamic keys.
        Args:
            key_dict: {}
                key_name (str): Redis key name
                key_value (str): Redis key value
            {
                "Name": John,
                "Location": "UK",
                "UUID": "1234"
            }
            dynamic = [Name, location, UUID]
            dynamic = aaaa:bbbb:cccc
        """
        dynamic_key_dict, dynamic_key = self.clean_key_dict_input(key_dict), ""
        upper_dynamic_keys = [str(k).upper() for k in dynamic_key_dict.keys()]
        if not len(dynamic_key_dict) == len(self.__schema.dynamics):
            message = "|".join(self.__schema.dynamics)
            raise RedisKeyError(
                f"Redis Dynamic Key Dictionary must have all key/keys: {message}"
            )
        for upper_dynamic_key in upper_dynamic_keys:
            dynamic_key += f"{key_dict[upper_dynamic_key]}{self.__delimiter}"
        self.__key = str(dynamic_key[:-1]).encode()

    @property
    def key(self):
        return self.__key.decode()

    # def get_expiry_time(self) -> int | None:
    #     """Calculate expiry time in seconds from kwargs."""
    #     time_multipliers = {"days": 86400, "hours": 3600, "minutes": 60, "seconds": 1}
    #     if self.expires_at:
    #         return sum(
    #             int(self.expires_at.get(unit, 0)) * multiplier
    #             for unit, multiplier in time_multipliers.items()
    #         )
    #     return None

    def feed(self, value: Union[bytes, Dict, List, str]) -> None:
        """
        Convert and store value in JSON format.

        Args:
            value: Value to store (bytes, dict, or list)

        Raises:
            RedisValueError: If value type is not supported

        Example:
            >>> RedisRow.feed({"name": "John", "age": 30})
            >>> RedisRow.feed(["value1", "value2"])
            >>> RedisRow.feed(b"Some Value to Store")
            >>> value_from_redis = RedisRow.value # Call by property
            '{"name": "John", "age": 30}'
        """
        try:
            if isinstance(value, (dict, list)):
                self.__value = json.dumps(value)
            elif isinstance(value, bytes):
                self.__value = json.dumps(json.loads(value.decode()))
            elif isinstance(value, str):
                self.__value = str(value)
            else:
                raise RedisValueError(f"Unsupported value type: {type(value)}")
        except json.JSONDecodeError as e:
            raise RedisValueError(f"Invalid JSON format: {str(e)}")


class MultipleRows:
    """
    Handles multiple RedisRow objects.

    This class provides methods for:
    - Managing multiple RedisRow objects
    - Bulk operations on RedisRow objects
    """

    __rows: List[RedisRow] = []

    def __init__(self, rows: List[RedisRow]):
        """
        Initialize MultipleRows with a list of RedisRow objects.
        Args:
            rows: List of RedisRow objects
        """
        self.__rows: List[RedisRow] = rows

    @property
    def all(self) -> List[RedisRow]:
        return list(self.__rows)

    @property
    def first(self) -> RedisRow:
        return list(self.__rows)[0]
