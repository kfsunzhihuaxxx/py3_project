#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:sunzhihua
@filename:demo2.py
@time:2021/4/18 16:36
@descirpt:async_demo2
"""

import asyncio


async def other():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


async def func():
    print("执行协程函数异步代码")
    response1 = await other()
    print("IO请求结束,结果为:", response1)
    response2 = await other()
    print("IO请求结束,结果为:", response2)


asyncio.run(func())
