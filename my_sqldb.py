# coding=utf-8
# coding=gbk

import MySQLdb
import sys
import uniout  # 没有这行就会出现数据库中无法读取中文
import time

time.localtime(time.time())
current_data = time.strftime('%Y%m%d', time.localtime(time.time()))


def init_db():
    connect = MySQLdb.connect(
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
        cur.execute('CREATE TABLE HouseInfo' + current_data + ' (address varchar(30),square varchar(30),money varchar(30),per_square VARCHAR (3))').fetchall()
        x = True
    except Exception as e:
        x = False
        print e
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
    pass


if __name__ == '__main__':
    print create_table()
