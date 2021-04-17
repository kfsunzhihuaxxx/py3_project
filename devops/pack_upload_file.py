#!/usr/bin/python3

"""
文件打包、上传与校验
我们时常做一些文件包分发的工作，实施步骤一般是先压缩打包，在批量上传至目标服务器，最后做一致性校验。
本示例通过put()方法实现文件的上传，通过对比本地与远程主机文件的md5，最终实现文件一致性校验。
"""


from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm


def host_type():
    run('uname -s')
