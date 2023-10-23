import subprocess
import redis
from jasonqwu_lib import *


class Redis:
    def __init__(self):
        self.start_redis()
        self.__pool = redis.ConnectionPool(host="127.0.0.1",
                                           port=6379,
                                           password="",
                                           decode_responses=True)

    def __del__(self):
        subprocess.Popen(['redis-server --service-uninstall'])

    def start_redis(self):
        try:
            # 启动Redis服务
            # exec("cd d:\\")
            subprocess.Popen(['redis-server'])
            debug("Redis服务已启动")
        except Exception as e:
            debug(f"启动Redis服务时出错: {e}")

    def open(self):
        self.__redis = redis.Redis(connection_pool=self.__pool)

    def close(self):
        self.redis.connection_pool.disconnect()

    @property
    def redis(self):
        return self.__redis

    def get(self, key):
        self.redis.get(key)

    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        """
           ex -> 失效时间，单位秒
           px -> 失效时间，单位毫秒
           nx -> 不存在时插入
           xx -> 存在时插入
        """
        self.redis.set(key, value)

    def print(self, key):
        debug(self.redis.ping())
        debug(self.redis.get(key))


if __name__ == '__main__':
    r = Redis()
    r.open()
    r.set("username", "张三")
    r.print("username")
    r.close()
    r.print("username")
