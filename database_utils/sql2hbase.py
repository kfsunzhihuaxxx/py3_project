#!/usr/bin/python3
# -*- coding=utf-8 -*-
# author:sunzhihua
# telephone:18911782528


"""
    此示例用来演示将localhost中的 sakila_dwh库的dim_actor,dim_customer,dim_date,dim_film,dim_film_actor_bridge,dim_staff,dim_store,dim_time
    fact_rental表导入到hadoop130中的 Hbase,用定时任务执行此文件,所以都没有print输出,运行日志都写到Import.logs文件里
"""

import happybase
import pymysql
import os
import json
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MAXRETRY = 5  # 连接断开时最大的尝试重新连接的次数
RETRYED = 0  # 已重连次数

# mysql连接配置
mysqlHost = "hadoop1"
mysqlUser = "root"
mysqlPwd = "123456"
mysqlDB = "sakila_dwh"
mysqlTable = ["dim_actor", "dim_customer", "dim_date", "dim_film", "dim_film_actor_bridge", "dim_staff", "dim_store",
              "dim_time", "fact_rental"]
mysqlPrimaryKey = "globaleventid_0"  # mysql主键,用该字段查数据,并作为hbase的rowkey

# hbase连接配置
HbaseHose = "192.0.50.118"
HbasePort = 9090
HbaseNamespace = "CABD"
HbaseTable = "gdelt_v2"
HbaseColFamily = "data"

# 运行日志及已导入量的记录, 如果任务中断了再次运行会自动读取导入量记录,不用从头开始导
basedir = os.path.dirname(os.path.abspath(__file__))
recordFile = os.path.join(basedir, "import_record.json")
logsFile = os.path.join(basedir, "Import.logs")
record = {}
if os.path.exists(recordFile):
    with open(recordFile, 'r') as f:
        record = json.load(f)
else:
    record = {
        "importedCount": 0,
        "importedID": 0,
    }
    with open(recordFile, 'w') as f:
        json.dump(record, f)

    # 发送邮件, 根据自己的邮箱进行配置即可, 因为我是用定时任务执行该脚本,


# 我希望出错时收到邮件,所以使用了邮件功能, 不需要的同学可以直接删掉这个函数
def sendEmail(msgToSend, receiver="673305066@qq.com"):
    # 配置
    smtpserver = 'smtphz.qiye.163.com'
    username = 'xxx@163.com'
    password = 'xxx'
    sender = 'xxx@163.com'
    receiver = [receiver, ]

    # 构造邮件对象MIMEMultipart对象
    # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
    msg = MIMEMultipart('mixed')
    msg['Subject'] = '定时任务出错'
    msg['From'] = 'xxx@163.com <xxx@163.com>'
    msg['To'] = ";".join(receiver)

    # 构造邮件
    html = '''
    <html lang="en">
    <head>
    </head>
    <body>
        <h3>尊敬的用户:</h3>
        <div style="padding-left: 30px">
            <p>%s</p>
        </div>
        <p style="color: gray;font-size:14px">--xxx皮包公司</p>

    </body>
    </html>
        ''' % msgToSend

    text_html = MIMEText(html, 'html', 'utf-8')
    msg.attach(text_html)

    # 发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver, 25)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


N = 1000  # 每次循环导入多少条记录
while (1):
    try:
        # 连接mysql
        db = pymysql.connect(host=mysqlHost, user=mysqlUser, password=mysqlPwd, db=mysqlDB, charset="utf8", port=3306)

        cur = db.cursor(pymysql.cursors.DictCursor)
        # 连接hbase
        connection = happybase.Connection(host=HbaseHose, port=HbasePort, timeout=None,
                                          autoconnect=True, table_prefix_separator=b':', compat='0.98',
                                          transport='buffered', protocol='binary',
                                          table_prefix=HbaseNamespace)
        lesi_table = connection.table(HbaseTable, use_prefix=True)
        RETRYED = 0
    except Exception as e:
        RETRYED += 1
        with open(logsFile, "a+", encoding='utf-8') as f:
            f.write("\n\nERROR(" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ") " + repr(
                e) + "\nRetry: " + str(RETRYED) + "/" + str(MAXRETRY) + "\n")
        if (RETRYED < MAXRETRY):
            continue
        else:
            with open(logsFile, "a+", encoding='utf-8') as f:
                f.write("\n\nERROR(" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ") " + repr(
                    e) + "\nExceeding the maximum retry times, exit process now!\n")
            # 发送邮件提醒
            msg = str("\n\n" + basedir + " Import ERROR(" + datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S") + ") " + repr(e) + "\nExceeding the maximum retry times, exit process now!\n")
            sendEmail(msg)
            os._exit(0)
    break

while (1):
    sql = """select * from """ + mysqlTable + """ where %s > %s order by %s asc limit %s;""" % (
        mysqlPrimaryKey, record["importedID"], mysqlPrimaryKey, N)
    cur.execute(sql)

    res = cur.fetchall()

    # 插入数据
    try:
        with lesi_table.batch() as bat:
            for r in res:
                ins_dic = {}
                for k in r.keys():
                    ins_dic[HbaseColFamily + ":" + k] = str(r[k])
                bat.put(str(r[mysqlPrimaryKey]), ins_dic)
                record["importedID"] = r[mysqlPrimaryKey]
        record["importedCount"] += len(res)
        with open(recordFile, 'w') as f:
            json.dump(record, f)
        with open(logsFile, "a+", encoding='utf-8') as f:
            f.write("INFO(" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ") 完成导入" + str(
                len(res)) + "条 当前RowKey:" + str(record["importedID"]) + " 总计已完成" + str(record["importedCount"]) + "条\n")

        if (len(res) < N):
            # 说明已经查到最后了, 此时应结束程序
            break
    except Exception as e:
        RETRYED += 1
        with open(logsFile, "a+", encoding='utf-8') as f:
            f.write("\n\nERROR(" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ") " + repr(
                e) + "\nRetry: " + str(RETRYED) + "/" + str(MAXRETRY) + "\n")
        if (RETRYED < MAXRETRY):
            # 出错重新连接
            try:
                cur.close()
                db.close()
                db = pymysql.connect(host=mysqlHost, user=mysqlUser, password=mysqlPwd, db=mysqlDB, charset="utf8",
                                     port=3306)
                cur = db.cursor(pymysql.cursors.DictCursor)
                # 连接hbase
                connection = happybase.Connection(host=HbaseHose, port=9090, timeout=None,
                                                  autoconnect=True, table_prefix_separator=b':', compat='0.98',
                                                  transport='buffered', protocol='binary',
                                                  table_prefix=HbaseNamespace)
                lesi_table = connection.table(HbaseTable, use_prefix=True)
            except Exception:
                continue
        else:
            with open(logsFile, "a+", encoding='utf-8') as f:
                f.write("\n\nERROR(" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ") " + repr(
                    e) + "\nExceeding the maximum retry times, exit process now!\n")
            # 发送邮件提醒
            msg = str("\n\n" + basedir + " Import ERROR(" + datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S") + ") " + repr(e) + "\nExceeding the maximum retry times, exit process now!\n")
            sendEmail(msg)
            os._exit(0)
cur.close()
db.close()
