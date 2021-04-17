#!/usr/bin/python3
# -*- coding=utf-8 -*-
# author:sunzhihua
# telephone:18911782528

"""
    该示例为服务器定时备份mysql数据库脚本
"""
import os
import datetime
import shutil
import subprocess
from multiprocessing import Process
import pymysql
from database_utils.dump_mysql_settings import *


# MODEL 层
class DumpDataBase:
    """服务器定时备份mysql数据库 脚本类"""

    def __init__(self, host, port, user, password, charset, dump_database_list, dump_abs_path, database=None):
        """初始化"""
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__charset = charset
        self.__dump_database_list = dump_database_list
        self.__dump_abs_path = dump_abs_path
        self.__database = database
        self.default_database_set = {'information_schema', 'mysql', 'performance_schema', 'sys'}

    def get_con_obj(self):
        """
        :return:游标
        """
        try:
            self.__conn = pymysql.Connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                passwd=self.__password,
                charset=self.__charset
            )
            self.__cur = self.__conn.cursor()
        except Exception as e:
            print(e, "连接有误，检查配置")
        return self.__cur

    def create_dump_dir(self):
        """
        :return: 返回要备份的绝对路径
        """
        if not os.path.exists(self.__dump_abs_path):
            try:
                os.mkdir(self.__dump_abs_path)
            except Exception as e:
                print('这个路径没有该文件夹,但帮你创建了一个,现在绝对有这个文件夹了')
            return self.__dump_abs_path
        else:
            return self.__dump_abs_path

    def create_timestamp(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        return timestamp

    def close_conn(self):
        """
        :return:None
        """
        self.__cur.close()
        self.__conn.close()
        return

    def get_container(self):
        """
        :return:返回要备份的列表,数据库里说有库的名称列表
        """
        self.__container = []
        query_databases_sql = "show databases;"
        self.__cur.execute(query_databases_sql)
        databases = [i[0] for i in self.__cur.fetchall()]
        for i in self.__dump_database_list:
            if i in databases:
                self.__container.append(i)
            else:
                print(i, '库不在该主机里，检查你要备份的库名是否在本主机')
                continue
        return self.__container, databases

    def move_tar_dir(self, timestamp, db_list):
        """
        :param db_list: 需要备份的列表
        :param timestamp:时间戳
        :return:None
        """
        new_dir = self.__dump_abs_path + '/' + timestamp
        if not os.path.exists(self.__dump_abs_path + '/' + timestamp):
            os.mkdir(self.__dump_abs_path + '/' + timestamp)
            for i in range(len(db_list)):
                file_name = self.__dump_abs_path + '/' + timestamp + "_" + db_list[i] + '.sql'
                print(file_name)
                shutil.move(file_name, new_dir)
        else:
            for i in range(len(db_list)):
                file_name = self.__dump_abs_path + '/' + timestamp + "_" + db_list[i] + '.sql'
                print(file_name)
                shutil.move(file_name, new_dir)
        tar_name = timestamp + '.tar.gz'
        tar_file = new_dir + '/*'
        res = subprocess.run(['tar', '-cvzf', tar_name, tar_file])
        if res == 0:
            # 执行成功
            print("备份打包完成！！！")
        else:
            print("拒绝备份空的归档！！！请检查你需要备份的库是否正确！")
        return

    def do_dump(self, db_name, timestamp):
        """
        :param timestamp: 时间戳
        :param db_name:容器列表
        :return:None
        """
        dump_sql = "mysqldump -uroot -h " + self.__host + " -p" + DUMP_DICT[
            "PASSWORD"] + " -P " + str(
            self.__port) + " --databases " + db_name + " --skip-add-locks --events --single-transaction > {}/{}_{}.sql;".format(
            self.__dump_abs_path,
            timestamp, db_name)
        print(dump_sql)
        try:
            os.system(dump_sql)
        except Exception as e:
            print(e, 'shell命令有误,检查命令')
        return


class MyDumpDataBase(DumpDataBase):
    """
    扩展API
    """

    def __init__(self):
        pass


# CORTROLLER 层
# 指定数据库备份函数
def appoint_backup_main():
    dump_db = DumpDataBase(host=DUMP_DICT['HOST'], port=DUMP_DICT['PORT'], user=DUMP_DICT['USER'],
                           password=DUMP_DICT['PASSWORD'], charset=DUMP_DICT['CHARSET'],
                           dump_database_list=DUMP_DATABASE_LIST, dump_abs_path=DUMP_ABS_PATH)
    cur = dump_db.get_con_obj()
    dump_path = dump_db.create_dump_dir()
    dump_list = dump_db.get_container()[0]
    print(dump_list)
    timestamp = dump_db.create_timestamp()
    print('备份列表:', dump_list)
    process_list = []
    for i in range(len(dump_list)):
        db_name = dump_list[i]
        print("db_name:", db_name)
        p = Process(target=dump_db.do_dump, args=(db_name, timestamp))
        process_list.append(p)
        p.start()  # 进程就绪开始
        print("Process {} end".format(str(i)))
    for i in process_list:
        i.join()  # 循环回收
    print("已生成backup文件！")
    try:
        new_dir = dump_db.move_tar_dir(timestamp, dump_list)
    except Exception as e:
        print(e, "文件夹重复创建,建议删除,从新运行")
    dump_db.close_conn()


# 除去配置文件中列表，指定内库之外，其余都备份的函数
def except_list_main():
    """
    attention: 此方法中 同样去读取dump_mysql_settings.py中的DUMP_DICT字典 和DUMP_DATABASE_LIST 但是此处的DUMP_DATABASE_LIST为
    指定在数据库系统中不备份，剩余都本分的列表，不要搞混！
    :return:
    """
    dump_db = DumpDataBase(host=DUMP_DICT['HOST'], port=DUMP_DICT['PORT'], user=DUMP_DICT['USER'],
                           password=DUMP_DICT['PASSWORD'], charset=DUMP_DICT['CHARSET'],
                           dump_database_list=DUMP_DATABASE_LIST, dump_abs_path=DUMP_ABS_PATH)
    cur = dump_db.get_con_obj()
    dump_path = dump_db.create_dump_dir()
    not_need_backup_list, databases = dump_db.get_container()
    not_need_backup_set = set(not_need_backup_list)
    databases_set = set(databases)
    need_backup_set = databases_set.difference(not_need_backup_set)
    need_backup_set = need_backup_set.difference(dump_db.default_database_set)
    dump_list = list(need_backup_set)
    timestamp = dump_db.create_timestamp()
    print('备份列表:', dump_list)
    process_list = []
    for i in range(len(dump_list)):
        db_name = dump_list[i]
        print("db_name:", db_name)
        p = Process(target=dump_db.do_dump, args=(db_name, timestamp))
        process_list.append(p)
        p.start()  # 进程就绪开始
        print("Process {} end".format(str(i)))
    for i in process_list:
        i.join()  # 循环回收
    print("已生成backup文件！")
    try:
        new_dir = dump_db.move_tar_dir(timestamp, dump_list)
    except Exception as e:
        print(e, "文件夹重复创建,建议删除,从新运行")
    dump_db.close_conn()


# 程序主入口
if __name__ == '__main__':
    operation_status_code = DUMP_DICT['status']
    # 0 表示指定库备份
    if operation_status_code == 0:
        appoint_backup_main()
    # 1 表示指定库备份
    elif operation_status_code == 1:
        except_list_main()
    else:
        pass
