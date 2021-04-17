#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021-04-12
# @Author  : sunzhihua
# @Site    : ~/py3_project
# @File    : psutil_tools.py
# @Software: PyCharm

import psutil
import matplotlib.pyplot as plt


class MyDevOps:
    def mem_issue(self):
        """
        :return:->dict:字典
        """
        # print('内存信息：')
        mem = psutil.virtual_memory()
        # 单位换算为MB
        memtotal = mem.total / 1024 / 1024
        memused = mem.used / 1024 / 1024
        memunused = memtotal - memused
        # print('内存使用大小:%.2fMB' % memused)
        # print('内存总大小:%.2fMB' % memtotal)

        return {"name": "mem", "data": {"memused": memused, "memunused": memunused}}

    def disk_list(self):
        """
        :return:->dict:字典
        """
        disk = psutil.disk_partitions()
        diskuse = psutil.disk_usage('/')
        # 单位换算为GB
        diskused = diskuse.used / 1024 / 1024 / 1024
        disktotal = diskuse.total / 1024 / 1024 / 1024
        diskunused = disktotal - diskused

        # print('磁盘使用大小:%.2fGB' % diskused)
        # print('磁盘总大小:%.2fGB' % disktotal)
        return {"name": "disk", "data": {"diskused": diskused, "diskunused": diskunused}}

    def cpu_used(self):
        cpu_used = psutil.cpu_percent()
        cpu_unused = 100 - cpu_used
        return {"name": "cpu", "data": {"cpu": cpu_used, "cpu_used": cpu_unused}}

    def create_plot(self, task_list):
        num=len(task_list)
        index=0
        for sub_number, data_dict in enumerate(task_list):
            index+=1
            name = data_dict['name']
            data = data_dict['data']
            labels = []
            fracs = []
            for item in data.items():
                labels.append(item[0])
                fracs.append(item[1])
            plt.subplot(1,num,index)
            plt.title(name)
            plt.pie(x=fracs, labels=labels, autopct="%0.f%%", shadow=True)
        plt.show()


if __name__ == '__main__':
    mydevops = MyDevOps()
    while True:
        cpu_dict = mydevops.cpu_used()
        disk_dict = mydevops.disk_list()
        mem_dict = mydevops.mem_issue()
        task_list = [cpu_dict, disk_dict, mem_dict]
        # print(task_list)
        mydevops.create_plot(task_list)
