from redis import Redis


class Cache:
    def __init__(self) -> None:
        self.redis_client: Redis = Redis(host="localhost", port=6379, db=0)

    def set(self, key, value):
        return self.redis_client.set(key, value)

    def get(self, key):
        return self.redis_client.get(key)


cache_instance = Cache()
