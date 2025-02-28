"""
Exceptions for the RedisMixin class.
"""


class RedisError(Exception):
    """Base exception for Redis-related errors."""

    pass


class RedisKeyError(RedisError):
    """Exception raised for Redis key-related errors."""

    pass


class RedisValueError(RedisError):
    """Exception raised for Redis value-related errors."""

    pass
