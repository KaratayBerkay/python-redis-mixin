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

Volumes:
    /redis/redis-master-data: Redis Master data storage
    /redis/replica1-data: Redis Replica 1 data storage
    /redis/replica2-data: Redis Replica 2 data storage

> Note: Delete and re-create directories if you encounter any permission issues. 

> Password protection for all Redis instances

> Persistent data storage with AOF

> Health checks

> Network isolation
All redis instances are isolated in the same network. This is useful for security and performance reasons over redis-network.
Commented TLS configuration options (uncomment if needed)

For production use, make sure to use a strong password and consider enabling the TLS options for encrypted connections.
