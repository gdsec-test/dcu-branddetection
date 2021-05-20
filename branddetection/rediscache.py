from dcustructuredloggingflask.flasklogger import get_logging
from redis import Redis


class RedisCache(object):
    """
    Redis helper class that handles storing and retrieving key/value pairs from the Redis instance
    """
    def __init__(self, settings):
        try:
            self._logger = get_logging()
            self.redis = Redis(settings.REDIS)
            self.redis_ttl = settings.REDIS_TTL
        except Exception as e:
            self._logger.fatal("Error in creating redis connection: %s", e)

    def get_value(self, redis_key):
        """
        Attempt to retrieve a value with key redis_key from the cache
        :param redis_key:
        :return:
        """
        try:
            redis_value = self.redis.get(redis_key)
        except Exception as e:
            self._logger.error("Error while retrieving {} : {}".format(redis_key, e))
            redis_value = None
        return redis_value

    def set_value(self, redis_key, redis_value):
        """
        Attempt to store a key/value pair in the cache with redis_ttl time to live
        :param redis_key:
        :param redis_value:
        :return:
        """
        try:
            self.redis.set(redis_key, redis_value)
            self.redis.expire(redis_key, self.redis_ttl)
        except Exception as e:
            self._logger.error("Error in setting the redis value for {} : {}".format(redis_key.decode('utf-8'), e))
