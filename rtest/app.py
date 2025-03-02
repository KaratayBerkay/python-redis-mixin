import time
from mixin.controller import redis_controller
from rtest.test_mixin import test_redis_actions

if __name__ == "__main__":
    print("Test service up and running")
    try:
        while True:
            print("write_cli.ping : ", redis_controller.write_cli.ping())
            print("read_cli.ping  : ", redis_controller.read_cli.ping())
            print("read_cli.ping  : ", redis_controller.read_cli.ping())
            test_redis_actions()
            time.sleep(100)
    except Exception as e:
        print("Error service : ", str(e))
