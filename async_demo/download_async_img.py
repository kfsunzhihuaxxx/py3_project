#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:sunzhihua
@filename:download_async_img.py
@time:2021/4/18 12:17
@descirpt:
"""
import asyncio
import aiohttp


async def fetch(session, url):
    print('发送请求', url)
    async with session.get(url, verify_ssl=False) as response:
        content = await response.content.read()
        numbers = (x for x in range(6))
        try:
            number = numbers.__next__()
        except Exception as e:
            filename = "OnePiece_" + str(number) + ".jpg"
            with open(filename, mode='wb') as file_object:
                file_object.write(content)
        filename = "OnePiece_" + str(number) + ".jpg"
        with open(filename, mode='wb') as file_object:
            file_object.write(content)


async def main():
    async with  aiohttp.ClientSession() as session:
        url_list = [
            "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2578059283,3786974076&fm=26&gp=0.jpg",
            "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2075472258,2986706346&fm=26&gp=0.jpg",
            "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=3192516745,2335093858&fm=26&gp=0.jpg",
            "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=740418155,2308237123&fm=26&gp=0.jpg",
            "https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=2778703682,2632588954&fm=26&gp=0.jpg",
            "https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=1756712057,3191802878&fm=26&gp=0.jpg",
            "https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=3908906577,4133291635&fm=26&gp=0.jpg",
            "https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=3275569617,4294256196&fm=26&gp=0.jpg",
        ]
        tasks = [
            asyncio.create_task(fetch(session, url)) for url in url_list
        ]


if __name__ == '__main__':
    asyncio.run(main())
