from config import redis_configs
from conn import RedisConn, Redis


class RedisController:

    __master_node = None
    __conn_pool: list = []
    __active_reader: int = 0

    def __init__(self, master_redis_config, replica_redis_configs: list):
        self.master_redis_config = master_redis_config
        self.replica_redis_configs = replica_redis_configs
        self.set_master_node()
        self.set_all_replicas()

    def set_master_node(self):
        """
        Create a connection to the master node.
        Returns:
            None
        """
        if not self.master_redis_config:
            raise Exception("No master configs are given to create a connection")
        try:
            master_node = RedisConn(
                dict(
                    host=redis_configs.HOST,
                    password=redis_configs.PASSWORD,
                    port=redis_configs.PORT,
                    db=redis_configs.DB
                )
            ).client
            if master_node.ping():
                self.__master_node = master_node
        except Exception as e:
            print(f"Redis Connection Error {redis_configs.master_redis_url} raised error : ", e)

    def set_all_replicas(self):
        """
        Create connections to all the replicas given in the configuration.
        Returns:
            None
        """
        if not self.replica_redis_configs:
            raise Exception("No replica configs are given to create connections")
        for _ in self.replica_redis_configs:
            replica_redis_cli = None
            try:
                replica_redis_cli = RedisConn(
                    dict(
                        host=redis_configs.REP_1_HOST,
                        password=redis_configs.REP_1_PASSWORD,
                        port=redis_configs.REP_1_PORT,
                        db=redis_configs.REP_1_DB
                    )
                ).client
            except Exception as e:
                print(f"Redis Connection Error {redis_configs.first_replica_url} raised error : ", e)
            if replica_redis_cli.ping():    # If replica node is connected successfully, add it to the pool
                self.__conn_pool.append(replica_redis_cli)
        if not self.replica_redis_configs:
            raise Exception("No replicas are created for the pool. Check the configurations.")

    @property
    def read_cli(self) -> Redis:
        """
        Ask for read client from the pool distributed in a round-robin fashion.
        Returns:
            Redis_Client: A Redis client for read operations.
        """
        if not self.__conn_pool:
            raise Exception("No replica connections are available")

        total_length = len(self.__conn_pool)
        if total_length == 1:    # If there is only one replica, return the same connection
            return self.__conn_pool[0]
        elif self.__active_reader + 1 < total_length:
            active_connection = self.__conn_pool[self.__active_reader]
            self.__active_reader += 1
            return active_connection
        else:
            active_connection = self.__conn_pool[self.__active_reader]
            self.__active_reader = 0
            return active_connection

    @property
    def write_cli(self) -> Redis:
        """
        Ask for write client from the pool. Master node is used for write operations.
        Returns:
            Redis_Client: A Redis client for write operations.
        """
        return self.__master_node


redis_replica_redis_configs = [
    dict(
        host=redis_configs.REP_1_HOST,
        password=redis_configs.REP_1_PASSWORD,
        port=redis_configs.REP_1_PORT,
        db=redis_configs.REP_1_DB
    ),
    dict(
        host=redis_configs.REP_2_HOST,
        password=redis_configs.REP_2_PASSWORD,
        port=redis_configs.REP_2_PORT,
        db=redis_configs.REP_2_DB
    )
]
master_config = dict(
    host=redis_configs.HOST,
    password=redis_configs.PASSWORD,
    port=redis_configs.PORT,
    db=redis_configs.DB
)
"""
Create a RedisController object to manage the master-replica setup. Singleton pattern is used to ensure only one
instance of the controller is created.
"""
redis_controller = RedisController(
    master_redis_config=master_config,
    replica_redis_configs=redis_replica_redis_configs
)
