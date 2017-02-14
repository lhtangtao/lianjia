# coding=utf-8
# coding=gbk

import MySQLdb
from xpinyin import Pinyin
import sys
import uniout  # 没有这行就会出现数据库中无法读取中文


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
    创建一张表，如果这个表存在的话则跳过
    :return: 如果存在 返回False，如果不存在则会建立一张表并且返回true
    """
    conn = init_db()
    cur = conn.cursor()
    try:
        cur.execute(
            'CREATE TABLE house_info (address varchar(30),square varchar(30),money varchar(30),per_square VARCHAR (3))').fetchall()
        x = True
    except:
        x = False
    cur.close()
    conn.commit()
    conn.close()
    return x


if __name__ == '__main__':
    print create_table()
