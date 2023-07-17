import redis
from datetime import datetime

class RedisTools:
    __redis_connect = redis.Redis(host='redis_stdx', port=6379)

    @classmethod
    def get_pair(cls, _id: datetime):
        return cls.__redis_connect.get(_id)
    
    @classmethod
    def hget_pair(cls, _id: datetime):
        return cls.__redis_connect.hget(_id)
    
    @classmethod
    def get_keys(cls):
        return cls.__redis_connect.keys(pattern='*')
    
    @classmethod
    def get_data(cls):
        return {k: cls.__redis_connect.get(k) for k in cls.get_keys()}