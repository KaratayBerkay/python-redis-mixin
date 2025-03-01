from mixin.mixins import redis_client
from mixin.schemas import RedisSchema
from print_actions import print_rows


# Create schema object to use at controller
schema_first = RedisSchema(
    static_keys=["STATIC_REDIS_KEY_1", "STATIC_REDIS_KEY_2", "STATIC_REDIS_KEY_3"],
    dynamic_keys=["DYNAMIC_KEY_1", "DYNAMIC_KEY_2", "DYNAMIC_KEY_3"],
    delimiter=":",
)


# Use client object to set schema
redis_client.set_schema(schema=schema_first)
redis_client.store(
    keys=["KeyToFind1", "KeyToFind2", "KeyToFind3"],
    value={"Name": "John", "Location": "UK", "UUID": "1234"},
    expires_at={"minutes": 10}
)


# Find a row with dynamic keys {"name": "value"} pair
multiple_rows = redis_client.find(keys_dict={"DYNAMIC_KEY_2": "KeyToFind1"})
print_rows(multiple_rows)
