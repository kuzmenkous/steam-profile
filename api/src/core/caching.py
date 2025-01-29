import redis_cli
import hashlib
import asyncio
import functools
import pickle

from typing import Any, Optional, Callable

from .config import settings


class RedisCaching:
    def __init__(self) -> None:
        self.redis = redis_cli.get_redis()

    @classmethod
    def init(cls):
        redis_cli.init_from_url(settings.redis.url)

    @classmethod
    def get_cache_key(
        cls,
        namespace: str = "",
        prefix: str = "",
    ) -> str:
        """
        Generates a cache key based on the prefix and namespace.
        """
        return f"{prefix}:{namespace}"

    async def _get_processed_value(self, value: Any) -> Any:
        return pickle.loads(value) if value else None

    async def get(self, key: str) -> Optional[Any]:
        value = self.redis.get(key)
        return await self._get_processed_value(value)

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = 15,
    ) -> None:
        value = pickle.dumps(value)
        if expire:
            self.redis.setex(key, expire, value)
        else:
            self.redis.set(key, value)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)


def init_caching():
    """Initialize the cache backend."""
    RedisCaching.init()


def cache(
    expire: int = 60,
    namespace: str = "",
    prefix: str = "",
    invalidate_keys: Optional[list[str]] = None,
) -> Callable:
    """
    Cache decorator to cache the result of the function.
    Works with both async and sync functions.
    """

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def inner(*args, **kwargs) -> Any:
            redis_caching = RedisCaching()
            cache_key = RedisCaching.get_cache_key(namespace, prefix)

            if invalidate_keys:
                for key in invalidate_keys:
                    await redis_caching.delete(key)

            cached_value = await redis_caching.get(cache_key)
            if cached_value:
                return cached_value

            if asyncio.iscoroutinefunction(func):
                res = await func(*args, **kwargs)
            else:
                res = func(*args, **kwargs)

            await redis_caching.set(cache_key, res, expire)
            return res

        return inner

    return wrapper
