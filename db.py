import redis

def set_up_redis(host, port):
    r = redis.Redis(host=host, port=port)
    return r