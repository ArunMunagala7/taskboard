from time import time
from typing import Optional

from fastapi import HTTPException, status, Request
from app.core.cache import get_redis


def _bucket_key(prefix: str, ident: str) -> str:
    return f"rl:{prefix}:{ident}"


def check_rate_limit(prefix: str, ident: str, limit: int, window_secs: int) -> None:
    """
    Sliding-window rate limit using Redis ZSET.
    Keeps timestamps for recent calls; prunes old; denies if count > limit.
    """
    now = int(time() * 1000)
    cutoff = now - (window_secs * 1000)

    r = get_redis()
    key = _bucket_key(prefix, ident)

    # prune old entries
    r.zremrangebyscore(key, 0, cutoff)

    # add this request and get current count
    pipe = r.pipeline()
    pipe.zadd(key, {str(now): now})
    pipe.zcard(key)
    pipe.expire(key, window_secs)  # auto-expire the set if idle
    _, count, _ = pipe.execute()

    if count > limit:
        # too many requests
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {limit} per {window_secs}s",
        )


# --------- Dependencies you can plug into routes ----------

def rl_login(request: Request) -> None:
    """
    Limit login attempts per IP: 10 requests / 60s
    """
    ip = request.client.host if request.client else "unknown"
    check_rate_limit("login_ip", ip, limit=10, window_secs=60)


def rl_task_list(user_id: int) -> None:
    """
    Limit task list per user: 120 requests / 300s (2 RPS avg)
    """
    check_rate_limit("tasklist_user", str(user_id), limit=120, window_secs=300)
