from redis import Redis



class RedisConn:

    def __init__(self):
        self.redis = Redis(**WagRedis.as_dict())
        if not self.check_connection():
            raise Exception("Connection error")

    def check_connection(self):
        return self.redis.ping()

    def set_connection(self, host, password, port, db):
        self.redis = Redis(host=host, password=password, port=port, db=db)
        return self.redis


try:
    redis_conn = RedisConn()
    redis_cli = redis_conn.redis
except Exception as e:
    print("Redis Connection Error", e)
