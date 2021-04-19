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


task_list = [
    func(),
    func()
]

done,pending = asyncio.run(asyncio.wait(task_list))
print(done)


