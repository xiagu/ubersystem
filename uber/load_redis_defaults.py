from uber.common import *

@entry_point
def load_redis_defaults():
    redis_config_key = 'dev'
    #redis_pool = ConnectionPool(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=int(os.environ['REDIS_DB']))
    redis_pool = ConnectionPool(host='127.0.0.1', port=6379, db=0)
    redis = StrictRedis(connection_pool=redis_pool)
    c = Dict(redis=redis, key=redis_config_key)

    print("foo",' ==> ',c.setdefault("foo", "testCon"))
