import base64
import hashlib
import json
from typing import Any
from loguru import logger

from app.redis_client import RedisClient


redis_client_local = RedisClient().connect()

def make_cache_key(raw_key: str) -> str:
    """Generate a unique cache key for a raw key."""
    return hashlib.sha256(raw_key.encode()).hexdigest()


def add_result_to_cache(key: str, value: Any, task_id: str | None = None, expire: int = 3600) -> None:
    """Cache a value + task_id to redis. Handles bytes by encoding to base64."""
    if isinstance(value, (bytes, bytearray)):
        value = base64.b64encode(value).decode("utf-8")  # encode bytes → str

    payload = {
        "result": value,
        "task_id": task_id,
    }
    # store payload in redis
    redis_client_local.set(key, json.dumps(payload, sort_keys=True), ex=expire)


def get_cached_result(key: str) -> tuple[Any, str | None]:
    """Get cached result from redis."""
    data = redis_client_local.get(key)

    if not data:
        logger.warning(f"Key {key} not found.")
        return None, None

    payload = json.loads(data)

    # attempt to decode if it looks like base64
    try:
        results_bytes = base64.b64decode(payload.get("result"))
        payload["result"] = results_bytes
    except Exception as e:
        logger.error(f"Error decoding base64 payload: {str(e)}")
        pass    # was just normal JSON serializable value

    return payload.get("result"), payload.get("task_id")








