import redis
from loguru import logger
from app.config import REDIS_URL


class RedisClient:
    def __init__(self, redis_url: str = REDIS_URL, decode_responses = True):
        self.redis_url = redis_url
        self.decode_responses = decode_responses
        logger.debug(f"Redis client running at {redis_url}")

    def connect(self):
        return redis.from_url(url=self.redis_url, decode_responses=self.decode_responses)


