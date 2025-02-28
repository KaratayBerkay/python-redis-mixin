from mixin.mixins import redis_client
from mixin.schemas import RedisSchema


# Create schema object to use at controller
schema_first = RedisSchema(
    static_keys=["STATIC_REDIS_KEY_1", "STATIC_REDIS_KEY_2", "STATIC_REDIS_KEY_3"],
    dynamic_keys=["DYNAMIC_KEY_1", "DYNAMIC_KEY_2", "DYNAMIC_KEY_3"],
    delimiter=":",
)

# Use client object to set schema
redis_client.set_schema(schema=schema_first)
multiple_rows = redis_client.find(keys_dict={"DYNAMIC_KEY_2": "KeyToFind"})

print('List of all rows (Keys) : ', [multiple_row.key for multiple_row in multiple_rows.all])
print('List of all rows (Data) : ', [multiple_row.data for multiple_row in multiple_rows.all])
print('First row        (Keys) : ', multiple_rows.first.key)
print('First row        (Data) : ', multiple_rows.first.data)
