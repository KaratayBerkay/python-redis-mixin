# python-redis-mixin
Python Redis MixinLike Library

Run all redis services de-attached
```bash
  docker compose up -d
```

Check services up and running
```bash
  docker-compose ps
```

This setup includes:
For production use, make sure to use a strong password and consider enabling the TLS options for encrypted connections.

# Excepted Container Outputs

- Redis Master Server Container Output
```python
2025-03-02 22:14:33 1:C 02 Mar 2025 19:14:33.641 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
2025-03-02 22:14:33 1:C 02 Mar 2025 19:14:33.641 * Redis version=7.2.7, bits=64, commit=00000000, modified=0, pid=1, just started
2025-03-02 22:14:33 1:C 02 Mar 2025 19:14:33.641 * Configuration loaded
2025-03-02 22:14:33 1:M 02 Mar 2025 19:14:33.642 * monotonic clock: POSIX clock_gettime
2025-03-02 22:14:33 1:M 02 Mar 2025 19:14:33.643 * Running mode=standalone, port=6379.
...
2025-03-02 22:14:39 14:C 02 Mar 2025 19:14:39.773 * Fork CoW for RDB: current 0 MB, peak 0 MB, average 0 MB
2025-03-02 22:14:39 1:M 02 Mar 2025 19:14:39.773 * Diskless rdb transfer, done reading from pipe, 2 replicas still up.
2025-03-02 22:14:39 1:M 02 Mar 2025 19:14:39.778 * Background RDB transfer terminated with success
2025-03-02 22:14:39 1:M 02 Mar 2025 19:14:39.779 * Streamed RDB transfer with replica 192.168.1.11:6380 succeeded (socket). Waiting for REPLCONF ACK from replica to enable streaming
2025-03-02 22:14:39 1:M 02 Mar 2025 19:14:39.779 * Synchronization with replica 192.168.1.11:6380 succeeded
2025-03-02 22:14:39 1:M 02 Mar 2025 19:14:39.779 * Streamed RDB transfer with replica 192.168.1.12:6381 succeeded (socket). Waiting for REPLCONF ACK from replica to enable streaming
2025-03-02 22:14:39 1:M 02 Mar 2025 19:14:39.779 * Synchronization with replica 192.168.1.12:6381 succeeded
```

- Redis Replica Container Output
```python
2025-03-02 22:14:34 1:C 02 Mar 2025 19:14:34.126 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
2025-03-02 22:14:34 1:C 02 Mar 2025 19:14:34.126 * Redis version=7.2.7, bits=64, commit=00000000, modified=0, pid=1, just started
2025-03-02 22:14:34 1:C 02 Mar 2025 19:14:34.126 * Configuration loaded
2025-03-02 22:14:34 1:S 02 Mar 2025 19:14:34.127 * monotonic clock: POSIX clock_gettime
2025-03-02 22:14:34 1:S 02 Mar 2025 19:14:34.128 * Running mode=standalone, port=6380.
2025-03-02 22:14:34 1:S 02 Mar 2025 19:14:34.129 * Server initialized
...
2025-03-02 22:14:34 1:S 02 Mar 2025 19:14:34.135 * MASTER <-> REPLICA sync started
2025-03-02 22:14:34 1:S 02 Mar 2025 19:14:34.135 * Non blocking connect for SYNC fired the event.
2025-03-02 22:14:34 1:S 02 Mar 2025 19:14:34.135 * Master replied to PING, replication can continue...
2025-03-02 22:14:34 1:S 02 Mar 2025 19:14:34.135 * Partial resynchronization not possible (no cached master)
2025-03-02 22:14:39 1:S 02 Mar 2025 19:14:39.770 * Full resync from master: 26413d827b4a41461e8a1db08aaff9eee33e50c9:251
2025-03-02 22:14:39 1:S 02 Mar 2025 19:14:39.772 * MASTER <-> REPLICA sync: receiving streamed RDB from master with EOF to disk
2025-03-02 22:14:39 1:S 02 Mar 2025 19:14:39.773 * MASTER <-> REPLICA sync: Flushing old data
2025-03-02 22:14:39 1:S 02 Mar 2025 19:14:39.773 * MASTER <-> REPLICA sync: Loading DB in memory
...
2025-03-02 22:14:39 1:S 02 Mar 2025 19:14:39.811 * Successfully renamed the temporary AOF base file temp-rewriteaof-bg-15.aof into appendonly.aof.29.base.rdb
2025-03-02 22:14:39 1:S 02 Mar 2025 19:14:39.811 * Successfully renamed the temporary AOF incr file temp-appendonly.aof.incr into appendonly.aof.29.incr.aof
2025-03-02 22:14:39 1:S 02 Mar 2025 19:14:39.815 * Removing the history file appendonly.aof.28.incr.aof in the background
2025-03-02 22:14:39 1:S 02 Mar 2025 19:14:39.815 * Removing the history file appendonly.aof.28.base.rdb in the background
2025-03-02 22:14:39 1:S 02 Mar 2025 19:14:39.820 * Background AOF rewrite finished successfully
```

## Redis easy use Mixin Library 
- Redis Mixin Container triggers function below
```python
def test_redis_actions():

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
        value={"Name": "John", "Location": "UK", "UUID": str(uuid4())},
        expires_at={"minutes": 10},
    )

    # Find a row with dynamic keys {"name": "value"} pair
    multiple_rows = redis_client.find(keys_dict={"DYNAMIC_KEY_2": "KeyToFind2"})
    print_rows(multiple_rows)
```

- Redis Mixin Container Output
```python
2025-03-02 22:14:38 Skipping virtualenv creation, as specified in config file.
2025-03-02 22:14:39 Test service up and running
2025-03-02 22:14:39 write_cli.ping :  True
2025-03-02 22:14:39 read_cli.ping  :  True
2025-03-02 22:14:39 read_cli.ping  :  True
2025-03-02 22:14:39 List of all rows (Keys) :  ['STATIC_REDIS_KEY_1:STATIC_REDIS_KEY_2:STATIC_REDIS_KEY_3:KeyToFind1:KeyToFind2:KeyToFind3']
2025-03-02 22:14:39 List of all rows (Data) :  [{'Name': 'John', 'Location': 'UK', 'UUID': '0e59ab32-6928-41a5-80b6-9c35be13dbd1'}]
2025-03-02 22:14:39 First row        (Keys) :  STATIC_REDIS_KEY_1:STATIC_REDIS_KEY_2:STATIC_REDIS_KEY_3:KeyToFind1:KeyToFind2:KeyToFind3
2025-03-02 22:14:39 First row        (Data) :  {'Name': 'John', 'Location': 'UK', 'UUID': '0e59ab32-6928-41a5-80b6-9c35be13dbd1'}
```