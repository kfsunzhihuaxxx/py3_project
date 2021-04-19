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
    print("main开始")
    task_list = [
        asyncio.create_task(func(),name='n1'),
        asyncio.create_task(func(),name='n2')
    ]
    done,pending = await asyncio.wait(task_list,timeout=None)
    print(done)

asyncio.run(main())
