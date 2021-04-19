#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:sunzhihua
@filename:demo8_thread_process_manager.py
@time:2021/4/19 12:24
@descirpt:concurrent.futures.Future对象
"""

import time
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor


def fun(value):
    time.sleep(1)
    print(value)
    return 123

# 创建线程池
pool = ThreadPoolExecutor(max_workers=5)

# 创建进程池
# pool = ProcessPoolExecutor(max_workers=5)


for i in range(10):
    fut = pool.submit(fun, i)
    print(fut)


