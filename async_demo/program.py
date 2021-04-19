#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:sunzhihua
@filename:program.py
@time:2021/4/17 11:30
@descirpt:
"""
import asyncio
import bs4
import aiohttp
from colorama import Fore


async def get_html(episode_number: int) -> str:
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f"https://talkpython.fm/{episode_number}"
    # resp = await requests.get(url)
    # resp.raise_for_status()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()

            html = await resp.text()

            return html


def get_title(html: str, episode_number: int) -> str:
    print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "MISSING"

    return header.text.strip()


async def get_title_range(loop):
    # please keep this range pretty small to not DDos my site.;
    tasks = []
    for n in range(185, 200):
        tasks.append((loop.create_task(get_html(n)), n))

    for task, n in tasks:
        html = await task
        title = get_title(html, n)
        print(Fore.WHITE + f"Title found:{title}", flush=True)


def main():
    # 创建asyncio异步对象
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_title_range(loop))

    print("Done.")





if __name__ == '__main__':
    main()
