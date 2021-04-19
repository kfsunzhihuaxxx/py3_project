#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:sunzhihua
@filename:demo9_spider.py
@time:2021/4/19 14:51
@descirpt:async_spider
"""

import asyncio
import requests


async def download_image(url):
    # 发送网络请求，下载图片(遇到网络下载图片的io请求，自动化切换到其他任务)
    print("开始下载:", url)

    loop = asyncio.get_event_loop()
    # requests模块默认不支持异步操作，所以就是用线程池来配合实现了。
    future = loop.run_in_executor(None, requests.get, url)

    response = await future
    print("下载完成")
    # 图片保存到本地文件
    # "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2578059283,3786974076&fm=26&gp=0.jpg"
    filename = url.split('/')[-1]
    with open(filename, mode='wb') as file_object:
        file_object.write(response.content)


if __name__ == '__main__':
    url_list = [
        "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2578059283,3786974076&fm=26&gp=0.jpg",
        "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2075472258,2986706346&fm=26&gp=0.jpg",
        "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=3192516745,2335093858&fm=26&gp=0.jpg",
        "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=740418155,2308237123&fm=26&gp=0.jpg",
        "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2778703682,2632588954&fm=26&gp=0.jpg",
        "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=1756712057,3191802878&fm=26&gp=0.jpg",
        "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=3908906577,4133291635&fm=26&gp=0.jpg",
        "https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=3275569617,4294256196&fm=26&gp=0.jpg"
    ]
    tasks = [download_image(url) for url in url_list]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


