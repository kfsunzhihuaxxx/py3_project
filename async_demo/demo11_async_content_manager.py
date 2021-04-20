#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:sunzhihua
@filename:demo11_async_content_manager.py
@time:2021/4/19 17:19
@descirpt:async content manager
"""

import asyncio


class AsyncContextManager:
    def __init__(self):
        self.conn = conn

    async def do_something(self):
        return 666

    async def __aenter__(self):
        # 异步连接数据库
        self.conn = await asyncio.sleep(1)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 异步关闭数据库连接
        await asyncio.sleep(1)


async def func():
    async with AsyncContextManager() as f:
        result = await f.do_something()
        print(result)


if __name__ == '__main__':
    asyncio.run(func())
