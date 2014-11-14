from uber.common import *

def setup_redis():
    redis_config_key = 'dev'
    #redis_pool = ConnectionPool(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=int(os.environ['REDIS_DB']))
    redis_pool = ConnectionPool(host='127.0.0.1', port=6379, db=0)
    redis = StrictRedis(connection_pool=redis_pool)
    c = Dict(redis=redis, key=redis_config_key)

@entry_point
def load_redis_defaults():
    setup_redis()

    defaults = Dict([
    ('foo', 'testCon'),
    ('bar', 'more stuff'),
    ('baz', 123),
    ])

    colorama.init()
    for key, value in defaults.items():
        current_value = c.get(key)
        if current_value == None:
            print(Back.YELLOW + Fore.WHITE + '[new]' +
                  Back.BLACK + Fore.YELLOW +
                  key.decode("utf-8") + ' ==> ' + str(value) +
                  Style.RESET_ALL
                  )
            c[key] = value
        elif current_value == value:
            print(Back.GREEN + Fore.WHITE + '[eql]' +
                  Back.BLACK + Fore.GREEN +
                  key.decode("utf-8") + ' ==> ' + str(value) +
                  Style.RESET_ALL
                  )
            pass
        else:
            print(Back.RED + Fore.WHITE + '[chg]' +
                  Back.BLACK + Fore.RED + ' [' + str(type(value)) + '] ' +
                  key.decode("utf-8") + ' ==> ' +
                  Back.RED + Fore.WHITE + '(not changed to: ' + str(value) +
                  ')' + Style.RESET_ALL
                  )

@entry_point
def print_redis_config():
    foo = pprint.pprint(c)
    print(foo)
