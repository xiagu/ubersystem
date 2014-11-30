from uber.common import *

def setup_redis():
    redis_config_key = 'dev'
    #redis_pool = ConnectionPool(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), db=int(os.environ['REDIS_DB']))
    redis_pool = ConnectionPool(host='127.0.0.1', port=6379, db=0)
    redis = StrictRedis(connection_pool=redis_pool)
    legacy = RedisDict(redis_config_key + '/legacy', redis, autosync=False)

@entry_point
def load_redis_defaults():
    setup_redis()


# Any configurable property defined in our configuration is automatically converted into a global constant,
# so outside of this file, we should never need to access this dictionary directly.  So we should prefer
# using the DONATIONS_ENABLED global constant instead of saying _config['donations_enabled'], etc.  See
# the comments in configspec.ini for explanations of the particular options, which are documented there.
# All global constants defined and exported here are also passed to our templates.
    defaults = parse_config(__file__)

    colorama.init()

    for key, value in defaults.items():
        # usually we'd just do this at the start of the request
        # but consistency is extra super important here
        legacy.sync()
        
        current_value = legacy.get(key)
        key_exists = legacy.__contains__(key)
        if not key_exists:
            print(Back.YELLOW + Fore.BLACK + '[new]' +
                  ' [' + str(type(current_value)) + ' ==> ' + str(type(value)) + '] ' +
                  Back.BLACK + Fore.YELLOW +
                  key + ' ==> ' + str(value) +
                  Style.RESET_ALL
                  )
            legacy[key] = value
        elif current_value == value:
            #print(Back.GREEN + Fore.WHITE + '[eql]' +
            #      ' [' + str(type(current_value)) + ' ==> ' + str(type(value)) + '] ' +
            #      Back.BLACK + Fore.GREEN +
            #      key + Style.RESET_ALL
            #      )
            pass
        else:
            print(Back.RED + Fore.WHITE + '[chg]' +
                  Back.BLACK + Fore.RED + ' [' + str(type(current_value)) + ' ==> ' + str(type(value)) + '] ' +
                  key + ' ==> ' +
                  Back.RED + Fore.WHITE + '(is: ' + str(current_value) + ' changed to: ' + str(value) +
                  ')' + Style.RESET_ALL
                  )
            legacy[key] = value

@entry_point
def print_redis_config():
    foo = pprint.pprint(legacy)
    print(foo)
