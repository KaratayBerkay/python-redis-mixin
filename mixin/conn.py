from redis import Redis
from config import redis_configs


class RedisConn:

    def __init__(self, config_dict):
        self.redis = Redis(**config_dict)
        if not self.check_connection():
            raise Exception("Connection error")

    def check_connection(self):
        return self.redis.ping()

    def set_connection(self, host, password, port, db):
        self.redis = Redis(host=host, password=password, port=port, db=db)
        return self.redis


master_redis_cli, first_replica_redis_cli, second_replica_redis_cli = None, None, None
replica_redis_pool = []

try:
    master_redis_conn = RedisConn(
        dict(
            host=redis_configs.HOST,
            password=redis_configs.PASSWORD,
            port=redis_configs.PORT,
            db=redis_configs.DB
        )
    )
    master_redis_cli = master_redis_conn.redis
except Exception as e:
    print(f"Redis Connection Error {redis_configs.master_redis_url} raised error : ", e)

try:
    first_replica_redis_cli = RedisConn(
        dict(
            host=redis_configs.REP_1_HOST,
            password=redis_configs.REP_1_PASSWORD,
            port=redis_configs.REP_1_PORT,
            db=redis_configs.REP_1_DB
        )
    ).redis
except Exception as e:
    print(f"Redis Connection Error {redis_configs.first_replica_url} raised error : ", e)

try:
    second_replica_redis_cli = RedisConn(
        dict(
            host=redis_configs.REP_2_HOST,
            password=redis_configs.REP_2_PASSWORD,
            port=redis_configs.REP_2_PORT,
            db=redis_configs.REP_2_DB
        )
    ).redis
except Exception as e:
    print(f"Redis Connection Error {redis_configs.second_replica_url} raised error : ", e)

for cli in [first_replica_redis_cli, second_replica_redis_cli]:
    if cli:
        replica_redis_pool.append(cli)

if not master_redis_cli:
    raise Exception("Master Redis Connection Error")

if len(replica_redis_pool):
    raise Exception("Replica Redis Connection Error")

print(
    f"Master Redis Connection: {master_redis_cli}\n"
    f"Total Replica Connections: {len(replica_redis_pool)}\n"
)