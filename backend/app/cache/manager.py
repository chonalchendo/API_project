from typing import Any

from redis import Redis


class Cache:
    def __init__(self) -> None:
        self.redis_client: Redis = Redis(host="localhost", port=6379, db=0)

    def set(self, key: str, value: Any):
        return self.redis_client.set(key, value)

    def get(self, key: str):
        return self.redis_client.get(key)

    def update(self, key: str, new_value: Any):
        return self.redis_client.setnx(key, new_value)


cache_instance = Cache()
