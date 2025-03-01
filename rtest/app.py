import time
from mixin.controller import redis_controller


if __name__ == "__main__":
    print('Test service up and running')
    try:
        while True:
            time.sleep(100)
            print('write_cli.ping : ', redis_controller.write_cli.ping())
            print('read_cli.ping  : ', redis_controller.read_cli.ping())
            print('read_cli.ping  : ', redis_controller.read_cli.ping())
    except Exception as e:
        print('Error service : ', str(e))
