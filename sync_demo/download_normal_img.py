#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
@author:sunzhihua
@filename:new_py.py
@time:2021/4/17 9:59
@descirpt:
"""

from datetime import datetime
import requests
from colorama import Fore


def dwonload_image(url_list):
    print(Fore.YELLOW + "开始下载")
    for idx in range(len(url_list)):
        response = requests.get(url_list[idx])
        file_name = "OnePiece_" + str(idx) + ".jpg"
        with open(file_name, 'wb') as f:
            f.write(response.content)
    print(Fore.CYAN + "下载完成")


if __name__ == '__main__':
    t0 = datetime.now()
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
    dwonload_image(url_list)
    dt = datetime.now() - t0
    print(Fore.WHITE + '一共用时:%.1f秒.' % (dt.total_seconds() * 10))
