from mixin.mixins import redis_client
from mixin.schemas import RedisSchema


# Create schema object to use at controller
schema_first = RedisSchema(
    static_keys=["STATIC_REDIS_KEY_1", "STATIC_REDIS_KEY_2", "STATIC_REDIS_KEY_3"],
    dynamic_keys=["DYNAMIC_KEY_1", "DYNAMIC_KEY_2", "DYNAMIC_KEY_3"],
)


# Use client object to set schema
redis_client.set_schema(schema=schema_first)
