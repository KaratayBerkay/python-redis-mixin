from redis import Redis


class RedisConn:
    """
    Connects to a Redis master-replica setup.

    Args:
        config_dict: A dictionary containing the Redis connection details.

    Returns:
        Creates a Redis connection object.
    """

    def __init__(self, config_dict):
        """
        Args:
            config_dict: RedisConfig = dict(
                host = str
                password = str
                port = int
                db = int
            )
        """
        self.redis = Redis(**config_dict)
        if not self.check_connection():
            raise Exception("Connection error")

    def check_connection(self):
        """
        Check if the connection is successful
        """
        return self.redis.ping()

    def set_connection(self, host, password, port, db) -> Redis:
        """
        Args:
            host: Hostname or IP address of the Redis server.
            password: Password for the Redis server.
            port: Port number of the Redis server.
            db: Database number to connect to.
        Returns:
            Set new config to redis and creates a new connection. Returns the Redis client object.
        """
        self.redis = Redis(host=host, password=password, port=port, db=db)
        return self.redis

    @property
    def client(self) -> Redis:
        """
            Returns the Redis client object.
        Returns:
        """
        return self.redis
