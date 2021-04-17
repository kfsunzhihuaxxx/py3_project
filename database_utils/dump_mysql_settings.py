"""
dump_mysql.py配置文件
author:sunzhihua
"""

# DUMP_DICT 为配置连接Mysql的基本信息
# "PORT"为主机地址,"PORT"为端口号,"USER"为用户,"PASSWORD"为密码,"DATABASE"为要查询的库名(也可以不写,缺省参数),"CHARSET"字符集
DUMP_DICT = {"status": 0, "HOST": "localhost", "PORT": 3306, "USER": "root", "PASSWORD": "123456", "CHARSET": "utf8"}
# DUMP_DICT = {"HOST": "", "PORT": "", "USER": "", "PASSWORD": "", "CHARSET": ""} # 默认都为空了 需要哪个主机就写那些主机

# DUMP_DATABASE_LIST 为你要在以上这个主机上想备份的库的名称列表
DUMP_DATABASE_LIST = ["sakila_dwh", "sakila"]
# DUMP_DATABASE_LIST = ["your_backup_database_name"]   # 在该列表里输入你要备份的库的名称


# DUMP_ABS_PATH 为你要将dump备份的.sql文件放在在本地哪个目录
DUMP_ABS_PATH = "/home/tarena/sunzhihua"
# DUMP_ABS_PATH = "/"   # 默认在/下
