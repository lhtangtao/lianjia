# coding=utf-8
# coding=gbk

# import MySQLdb
import pymysql
import sys
import uniout  # 没有这行就会出现数据库中无法读取中文
import time

time.localtime(time.time())
current_data = time.strftime('%Y%m%d', time.localtime(time.time()))


def init_db():
    """
    请在此处输入数据库的信息
    :return:
    # """
    # connect = MySQLdb.connect(
    connect = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        db='test',
        charset="utf8",  # 确保没有乱码
        passwd='root'
    )
    assert isinstance(connect, object)
    return connect


def create_table():
    """
    创建一张表，如果这个表存在的话则跳过 必须要确保数据库名字为test且存在
    :return: 如果存在 返回False，如果不存在则会建立一张表并且返回true
    """
    conn = init_db()
    cur = conn.cursor()
    try:
        sql_script = 'CREATE TABLE houseinfo' + current_data + ' (Id varchar(30),current_data varchar(30),location varchar(30),village varchar(30),house_type varchar(30),square varchar(30),orientation varchar(30), decorate varchar(30),money varchar(30),per_square VARCHAR (30),url varchar(300),page varchar(30))'
        cur.execute(sql_script)
        sql_script = "ALTER TABLE `test`.`houseinfo" + current_data + "` MODIFY COLUMN `Id` int(30) NOT NULL FIRST,MODIFY COLUMN `square` int(30) NULL DEFAULT NULL AFTER `house_type`,MODIFY COLUMN `money` int(30) NULL DEFAULT NULL AFTER `decorate`,MODIFY COLUMN `per_square` int(30) NULL DEFAULT NULL AFTER `money`,MODIFY COLUMN `page` int(30) NULL DEFAULT NULL AFTER `url`,ADD PRIMARY KEY (`Id`);"
        cur.execute(sql_script)
        x = True
    except Exception as e:
        x = False
        print e
        sql_script = "truncate table houseinfo" + current_data
        cur.execute(sql_script)
    cur.close()
    conn.commit()
    conn.close()
    return x


def insert_info(kind, value):
    """
    要插入的数据列名和数值
    :param kind:
    :param value:
    :return:
    """
    conn = init_db()
    cur = conn.cursor()
    try:
        sql_script0 = "INSERT INTO houseinfo%s" % current_data
        sql_script1 = "(%s) VALUES " % kind
        sql_script2 = "('%s')" % value
        sql_script = sql_script0 + sql_script1 + sql_script2
        # print sql_script
        cur.execute(sql_script)
        x = True
    except Exception as e:
        x = False
        print e
    cur.close()
    conn.commit()
    conn.close()
    return x


def update_info(kind, value, id_num):
    conn = init_db()
    cur = conn.cursor()
    try:
        sql_script0 = "UPDATE houseinfo%s SET" % current_data
        sql_script1 = " %s =" % kind
        sql_script2 = "('%s')" % value
        sql_script3 = "where id='%s'" % id_num
        sql_script = sql_script0 + sql_script1 + sql_script2 + sql_script3
        # print sql_script
        cur.execute(sql_script)
        x = True
    except Exception as e:
        x = False
        print e
    cur.close()
    conn.commit()
    conn.close()
    return x


def get_row():
    """
    获取目前的数据库的行数
    :return:
    """
    conn = init_db()
    cur = conn.cursor()
    sql_script = 'SELECT * FROM houseinfo%s' % current_data
    # sql_script = 'SELECT * FROM houseinfo20170216'
    # print sql_script
    row = cur.execute(sql_script)
    cur.close()
    conn.commit()
    conn.close()
    return row


if __name__ == '__main__':
    print create_table()
    print get_row()
