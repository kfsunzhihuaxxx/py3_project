#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:sunzhihua
@filename:demo3.py
@time:2021/4/18 16:58
@descirpt:
"""

import asyncio


async def func():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


async def main():
    task1 = asyncio.create_task(func())
    task2 = asyncio.create_task(func())
    print("main结束")

    ret1 = await task1
    ret2 = await task2
    print(ret1, ret2)


asyncio.run(main())
