from redis import Redis
from redis.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError, TimeoutError, AuthenticationError


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
        try:
            self.redis = Redis(
                **config_dict,
                retry=Retry(ExponentialBackoff(cap=5.12, base=0.1), retries=5),
                retry_on_timeout=True,
                retry_on_error=[ConnectionError, TimeoutError]
            )
        except AuthenticationError as e:
            print(f"Redis Authentication error: {e}")
        except ConnectionError as e:
            print(f"Redis Connection error: {e}")
        except Exception as e:
            print(f"Redis Error: {e}")
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
        """
        return self.redis
