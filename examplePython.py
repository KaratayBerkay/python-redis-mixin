import redis


def connect_redis(master_host="redis-master", master_port=6379, replica_hosts=["redis-replica-1", "redis-replica-2"], replica_port=6379, password=None):
    """
    Connects to a Redis master-replica setup.

    Args:
        master_host: Hostname of the Redis master.
        master_port: Port of the Redis master.
        replica_hosts: List of hostnames of Redis replicas.
        replica_port: Port of the Redis replicas.
        password: Optional password for Redis authentication.

    Returns:
        A tuple containing the Redis master connection and a list of Redis replica connections.
    """

    try:
        if password:
            master_conn = redis.Redis(host=master_host, port=master_port, password=password, decode_responses=True)
        else:
            master_conn = redis.Redis(host=master_host, port=master_port, decode_responses=True)
        master_conn.ping()  # Check if the master connection is successful
        print(f"Connected to Redis master at {master_host}:{master_port}")

        replica_conns = []
        for replica_host in replica_hosts:
            try:
                if password:
                    replica_conn = redis.Redis(host=replica_host, port=replica_port, password=password, decode_responses=True)
                else:
                    replica_conn = redis.Redis(host=replica_host, port=replica_port, decode_responses=True)

                replica_conn.ping() #check if replica connection is succesful
                replica_conns.append(replica_conn)
                print(f"Connected to Redis replica at {replica_host}:{replica_port}")
            except redis.exceptions.ConnectionError as e:
                print(f"Error connecting to Redis replica {replica_host}: {e}")

        return master_conn, replica_conns

    except redis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis master: {e}")
        return None, None

def write_to_redis(master_conn, key, value):
    """Writes data to the Redis master."""
    if master_conn:
        try:
            master_conn.set(key, value)
            print(f"Wrote '{key}': '{value}' to Redis master.")
        except redis.exceptions.RedisError as e:
            print(f"Error writing to Redis master: {e}")

def read_from_redis(replica_conns, key):
    """Reads data from a Redis replica (randomly selects one)."""
    if replica_conns:
        import random
        replica_conn = random.choice(replica_conns)
        try:
            value = replica_conn.get(key)
            print(f"Read '{key}': '{value}' from Redis replica.")
            return value
        except redis.exceptions.RedisError as e:
            print(f"Error reading from Redis replica: {e}")
            return None

# Example usage:
master, replicas = connect_redis(password="yourpassword") #add your password if you configured one.
if master:
    write_to_redis(master, "mykey", "myvalue")
if replicas:
    read_from_redis(replicas, "mykey")
