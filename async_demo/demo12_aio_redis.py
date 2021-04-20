#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:sunzhihua
@filename:demo12_aio_redis.py
@time:2021/4/20 16:44
@descirpt:async interact redis
"""

import asyncio
import aioredis


async def execute(address, password):
    print("开始执行", address)
    # 网络IO操作:创建redis连接
    redis = await aioredis.create_redis(address, password=password)

    # 网络IO操作:在redis中设置哈希值car,内部在设三个键值对,即:redis = {car:{key1:1,key2:2,key3:3}}
    await redis.hmset_dict("car", key1=1, key2=2, key3=3)

    # 网络IO操作:去redis中获取值
    result = await redis.hgetall("car",encoding="utf-8")
    print(result)

    redis.close()
    # 网络IO操作:关闭redis连接

    print("结束",address)


asyncio.run(execute('redis:127.0.0.1:6379'))
