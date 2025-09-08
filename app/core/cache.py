import json
from typing import Any
import redis
from app.core.config import settings

_redis = None  # module-level singleton

def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        # decode_responses=True => str in/out
        _redis = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis

def cache_get(key: str) -> Any | None:
    raw = get_redis().get(key)
    return None if raw is None else json.loads(raw)

def cache_set(key: str, value: Any, ttl: int = 60) -> None:
    get_redis().set(key, json.dumps(value), ex=ttl)

def cache_delete_pattern(pattern: str) -> int:
    r = get_redis()
    n = 0
    for k in r.scan_iter(pattern):
        r.delete(k)
        n += 1
    return n
