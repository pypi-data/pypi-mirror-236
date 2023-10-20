from redis.asyncio import Redis
from async_direct_redis.functions import *


class AsyncDirectRedis(Redis):
    async def keys(self, pattern: str = "*"):
        encoded = await super().keys(pattern)
        return [convert_get_type(key, pickle_first=False) for key in encoded]

    async def randomkey(self, pickle_first=False):
        encoded = await super().randomkey()
        return convert_get_type(encoded, pickle_first)

    async def type(self, name):
        encoded = await super().type(name)
        return convert_get_type(encoded, pickle_first=False)

    async def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        return await super().set(key, convert_set_type(value))

    async def get(self, key, pickle_first=False):
        encoded = await super().get(key)
        return convert_get_type(encoded, pickle_first)

    async def mset(self, mapping):
        if not isinstance(mapping, dict):
            raise Exception("mapping must be a python dictionary")
        else:
            mapping = convert_set_mapping_dic(mapping)
            return await super().mset(mapping)

    async def mget(self, *args, pickle_first=False):
        encoded = await super().mget(args)
        return [convert_get_type(value, pickle_first) for value in encoded]

    async def hkeys(self, name):
        encoded = await super().hkeys(name)
        return [convert_get_type(key, pickle_first=False) for key in encoded]

    async def hset(self, name, key, value):
        return await super().hset(name, key, convert_set_type(value))

    async def hmset(self, name, mapping):
        if not isinstance(mapping, dict):
            raise Exception("mapping must be a python dictionary")
        else:
            mapping = convert_set_mapping_dic(mapping)
            return await super().hmset(name, mapping)

    async def hget(self, name, key, pickle_first=False):
        encoded = await super().hget(name, key)
        return convert_get_type(encoded, pickle_first)

    async def hmget(self, name, *keys, pickle_first=False):
        encoded = await super().hmget(name, *keys)
        return [convert_get_type(value, pickle_first) for value in encoded]

    async def hvals(self, name, pickle_first=False):
        encoded = await super().hvals(name)
        return [convert_get_type(value, pickle_first) for value in encoded]

    async def hgetall(self, name, pickle_first=False):
        encoded = await super().hgetall(name)
        dic = dict()
        for k, v in encoded.items():
            new_k = k.decode('utf-8')
            dic[new_k] = convert_get_type(v, pickle_first)
        return dic

    async def sadd(self, name, *values):
        encoded = [convert_set_type(value) for value in values]
        return await super().sadd(name, *encoded)

    async def srem(self, name, *values):
        encoded = [convert_set_type(value) for value in values]
        return await super().srem(name, *encoded)

    async def sismember(self, name, value):
        encoded = convert_set_type(value)
        return await super().sismember(name, encoded)

    async def smembers(self, name, pickle_first=False):
        encoded = await super().smembers(name)
        return {convert_get_type(value, pickle_first) for value in encoded}

    async def spop(self, name, pickle_first=False):
        encoded = await super().spop(name)
        return convert_get_type(encoded, pickle_first)

    async def srandmember(self, name, count=None, pickle_first=False):
        encoded = await super().srandmember(name, number=count)
        if isinstance(encoded, list):
            return [convert_get_type(value, pickle_first) for value in encoded]
        else:
            return convert_get_type(encoded, pickle_first)

    async def sdiff(self, primary_set, *comparing_sets):
        encoded = await super().sdiff(primary_set, *comparing_sets)
        return {convert_get_type(value, pickle_first=False) for value in encoded}

    async def lpush(self, name, *values):
        encoded = [convert_set_type(value) for value in values]
        return await super().lpush(name, *encoded)

    async def lpushx(self, name, value):
        return await super().lpushx(name, convert_set_type(value))

    async def rpushx(self, name, value):
        return await super().rpushx(name, convert_set_type(value))

    async def rpush(self, name, *values):
        encoded = [convert_set_type(value) for value in values]
        return await super().rpush(name, *encoded)

    async def lpop(self, name, pickle_first=False):
        encoded = await super().lpop(name)
        return convert_get_type(encoded, pickle_first)

    async def rpop(self, name, pickle_first=False):
        encoded = await super().rpop(name)
        return convert_get_type(encoded, pickle_first)

    async def lindex(self, name, index, pickle_first=False):
        encoded = await super().lindex(name, index)
        return convert_get_type(encoded, pickle_first)

    async def lrange(self, name, start=0, end=-1, pickle_first=False):
        """
        If start and end are not defined, returns everything.
        :param str name: key name
        :param int start: starting index. default 0: first index
        :param int end: ending index. default -1: ending index
        :param bool pickle_first: forcing deserialize rather than decoding utf-8
        :return: list
        """
        encoded = await super().lrange(name, start, end)
        return [convert_get_type(value, pickle_first) for value in encoded]
