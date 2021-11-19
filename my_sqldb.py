# coding=utf-8
# coding=gbk

# import MySQLdb
import pymysql
import sys
import uniout  # 没有这行就会出现数据库中无法读取中文
import time

time.localtime(time.time())
current_date = time.strftime('%Y_%m_%d', time.localtime(time.time()))
table_name = 'lianjia'


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
        db='lianjia',
        charset="utf8",  # 确保没有乱码
        passwd='root'
    )
    assert isinstance(connect, object)
    return connect


def create_table(drop=True):
    """
    创建一张表，如果这个表存在的话则跳过 必须要确保数据库名字为test且存在
    :return: 如果存在 返回False，如果不存在则会建立一张表并且返回true
    """
    conn = init_db()
    cur = conn.cursor()
    try:
        sql_script = 'CREATE TABLE ' + table_name + ' (date varchar(30),city varchar(30),location varchar(30),sub_location varchar(30),village varchar(30),house_type varchar(30),square varchar(30),orientation varchar(30), decorate varchar(30),money varchar(30),per_square VARCHAR (30),url varchar(300),page varchar(30))'
        print u'first sql ' + sql_script
        cur.execute(sql_script)
        sql_script = "ALTER TABLE `lianjia`.`" + table_name + "`MODIFY COLUMN `square` int(30) NULL DEFAULT NULL AFTER `house_type`,MODIFY COLUMN `money` int(30) NULL DEFAULT NULL AFTER `decorate`,MODIFY COLUMN `per_square` int(30) NULL DEFAULT NULL AFTER `money`,MODIFY COLUMN `page` int(30) NULL DEFAULT NULL AFTER `url`,ADD PRIMARY KEY (`url`,`date`);"
        cur.execute(sql_script)
        print u"second sql" + sql_script
        x = True
    except Exception as e:
        x = False
        print u"！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！出现报错请查看错误原因"
        print e
        print u"错误打印完毕！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！"
        if drop == True:
            sql_script = "drop table " + table_name
            cur.execute(sql_script)
            print u"third " + sql_script
            create_table()
    cur.close()
    conn.commit()
    conn.close()
    return x


def insert_info(value):
    """
    要插入的数据列名和数值
    :param value:
    :return:
    """
    conn = init_db()
    cur = conn.cursor()
    try:
        sql_script0 = "INSERT INTO %s" % table_name
        sql_script1 = ' (date,city,location,sub_location,village,house_type,square,orientation,decorate,money,' \
                      'per_square,url,page,source_url) VALUES '
        sql_script2 = "(%s)" % value
        sql_script = sql_script0 + sql_script1 + sql_script2
        cur.execute(sql_script)
    except Exception as e:
        pass
    cur.close()
    conn.commit()
    conn.close()
    # print sql_script
    return sql_script


def get_row():
    """
    获取目前的数据库的行数
    :return:
    """
    conn = init_db()
    cur = conn.cursor()
    sql_script = 'SELECT  * FROM %s' % table_name
    print sql_script
    row = cur.execute(sql_script)
    cur.close()
    conn.commit()
    conn.close()
    # return row


if __name__ == '__main__':
    print create_table(False)
