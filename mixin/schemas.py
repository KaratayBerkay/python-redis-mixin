from typing import Union
from errors import RedisKeyError


class RedisSchema:

    __static_keys: list = []
    __dynamic_keys: list = []
    __delimiter: str = ":"

    def __init__(self, static_keys: list, dynamic_keys: list):
        """
        Initialize RedisKeys with static keys. Set dynamic keys via set_keys method.
        Args:
            static_keys: STATIC_REDIS_KEY_1, STATIC_REDIS_KEY_2, STATIC_REDIS_KEY_3
            dynamic_keys: DYNAMIC_KEY_1, DYNAMIC_KEY_2, DYNAMIC_KEY_3

        Example:
            >>> redis_key = RedisSchema(
            >>> static_keys=["STATIC_REDIS_KEY_1", "STATIC_REDIS_KEY_2", "STATIC_REDIS_KEY_3"],
            >>> dynamic_keys=["DYNAMIC_KEY_1", "DYNAMIC_KEY_2", "DYNAMIC_KEY_3"]
            >>> )
        """
        if not static_keys:
            raise RedisKeyError(
                "Static keys are required to create dynamic search with keys."
            )

        if not dynamic_keys:
            raise RedisKeyError(
                "Dynamic keys are required to create dynamic search with keys."
            )

        self.__static_keys = static_keys
        self.__dynamic_keys = dynamic_keys

    @property
    def dynamics(self):
        """
        Get dynamic keys.
        Returns:
            [str]: List of dynamic keys
        """
        return self.__dynamic_keys

    @property
    def statics(self):
        """
        Get static keys.
        Returns:
            [str]: List of static keys
        """
        return self.__static_keys

    @property
    def category(self) -> str:
        """
        Generate category keys for Redis.
        Returns:
            Returns a string of static keys separated by given delimiter
            STATIC_REDIS_KEY_1:STATIC_REDIS_KEY_2:STATIC_REDIS_KEY_3
        """
        return ":".join([_ for _ in self.statics])

    @property
    def search_keys(self) -> str:
        """
        Generate search keys for Redis.
        Returns:
            Returns a string of dynamic keys separated by given delimiter
            DYNAMIC_KEY_1:DYNAMIC_KEY_2:DYNAMIC_KEY_3
        """
        return ":".join([_ for _ in self.dynamics])

    @property
    def redis_key(self) -> bytes:
        """
        Returns:
            Returns a string of static and dynamic keys separated by given delimiter
        """
        return str(self.category + self.search_keys).encode()

    def set_keys(self, dynamic_keys: Union[list[str], str]) -> None:
        """
        Set dynamic keys for Redis search.
        Args:
            dynamic_keys:
        """
        if isinstance(dynamic_keys, str):
            if dynamic_keys not in self.__dynamic_keys:
                self.__dynamic_keys.append(dynamic_keys)
        elif isinstance(dynamic_keys, list):
            for _ in dynamic_keys:
                if _ not in self.__dynamic_keys:
                    self.__dynamic_keys.append(_)
