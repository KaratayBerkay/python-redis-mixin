from typing import Union
from errors import RedisKeyError


class RedisSchema:

    __static_keys: list = []
    __dynamic_keys: list = []
    __delimiter: str = ":"

    def __init__(self, static_keys: list, dynamic_keys: list, delimiter: str = ":"):
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
        self.__delimiter = delimiter
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
    def delimiter(self):
        """
        Get delimiter.
        Returns:
            str: Delimiter
        """
        return self.__delimiter

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
                str(k).upper() for k in self.dynamics
            ):
                if str(self.__delimiter) in str(key_dict[key_dyn]):
                    raise RedisKeyError(
                        f"Key value cannot contain delimiter: {self.__delimiter}"
                    )
                dynamic_key_dict[str(key_dyn).upper()] = key_dict[key_dyn]
        return dynamic_key_dict

    def merge_key(self, key_dict: dict) -> str:
        """
        Merge key with dynamic keys.
        Args:
            key_dict: Dictionary of keys
        """
        dynamic_key_dict, dynamic_key = self.clean_key_dict_input(key_dict), ""
        upper_dynamic_keys = [str(k).upper() for k in dynamic_key_dict.keys()]
        for upper_dynamic_key in upper_dynamic_keys:
            key_to_set = "*"
            if upper_dynamic_key in key_dict:
                key_to_set = key_dict[upper_dynamic_key]
            dynamic_key += f"{key_to_set}{self.__delimiter}"
        return str(dynamic_key[:-1])
