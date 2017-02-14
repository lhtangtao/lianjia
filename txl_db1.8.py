# coding=utf-8
# coding=gbk

import MySQLdb
from xpinyin import Pinyin
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
import uniout


def init_db():
    conn = MySQLdb.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        db='test',
        charset="utf8",  # 确保没有乱码
        passwd='root'
    )
    return conn


def db_find_all():  # 把所有的数据读取到一个二维数组
    conn = init_db()
    cur = conn.cursor()
    # cur.execute("create table 35txl(id int ,name varchar(20),telephone bigint(11))") #创建表
    cur.execute("select * from 35txl")
    x = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return x


def show_all():  # 显示所有人的数据
    conn = init_db()
    cur = conn.cursor()
    # cur.execute("create table 35txl(id int ,name varchar(20),telephone bigint(11))") #创建表
    row = cur.execute("select * from 35txl")  # 显示这个数据表有多少行
    x = cur.fetchall()  # x是个二维数组，里面有全部的数据库信息
    i = 0
    while i < row:
        y = x[i][0]
        y1 = x[i][1]
        y2 = x[i][2]
        y3 = x[i][3]
        print("%s %s %s %s" % (y, y1, y2, y3))
        i = i + 1
    cur.close()
    conn.commit()
    conn.close()
    print(" ")


def db_find_row_name(name):  # 根据名字查找电话号码，返回电话号码 本函数只适合没有重名的情况
    conn = init_db()
    cur = conn.cursor()
    sqlscript = "select 0* from 35txl where name like '%%%s%%'" % name
    row = cur.execute(sqlscript)
    x = cur.fetchall()
    i = 0
    n = 1
    zon = []
    while (i < row):
        n = 1
        while (n < 3):
            y = x[i][n]
            n = n + 1
            zon.append(y)
        i = i + 1
    cur.close()
    conn.commit()
    conn.close()
    return zon  # 返回的数组 格式为奇数为名字，偶数为电话号码


def db_find_row_tel(tel):  # 根据电话号码查找名字，返回名字 本函数只适合没有重名的情况
    conn = init_db()
    cur = conn.cursor()
    sqlscript = "select * from 35txl where telephone like '%%%s%%'" % tel
    row = cur.execute(sqlscript)
    x = cur.fetchall()
    i = 0
    n = 1
    zon = []
    while (i < row):
        n = 1
        while (n < 3):
            y = x[i][n]
            n = n + 1
            zon.append(y)
        i = i + 1
    cur.close()
    conn.commit()
    conn.close()
    return zon  # 返回的数组 格式为奇数为名字，偶数为电话号码


def db_find_row_sn(sn):  # 根据缩写查找电话号码，返回电话号码 本函数可解决重名的情况
    conn = init_db()
    cur = conn.cursor()
    sqli = "select * from 35txl where shortname=%s"  # 35txl为表名
    row = cur.execute(sqli, (sn))
    x = cur.fetchall()
    i = 0
    zon = []
    while (i < row):
        y = x[i][2]
        i = i + 1
        zon.append(y)
    cur.close()
    conn.commit()
    conn.close()
    return zon


def db_set_tel(NO, tel):  # 根据id修改电话号码函数
    conn = init_db()
    cur = conn.cursor()
    sqli = "update 35txl set telephone=%s where id=%s"  # 35txl为表名
    tel = int(tel)
    NO = int(NO)
    row = cur.execute(sqli, (tel, NO))
    cur.close()
    conn.commit()
    conn.close()
    return row


def auto_id():
    conn = init_db()
    cur = conn.cursor()
    row = cur.execute("select * from 35txl")
    cur.close()
    conn.commit()
    conn.close()
    z = row + 1
    return z


def db_set_name(NO, name):  # 根据id修改名字函数
    conn = init_db()
    cur = conn.cursor()
    sqli = "update 35txl set name=%s where id=%s"  # 35txl为表名
    NO = int(NO)
    row = cur.execute(sqli, (name, NO))
    cur.close()
    conn.commit()
    conn.close()
    return row


def db_insert(NO, name, tel, shortname):  # 添加新的人员的信息
    conn = init_db()
    cur = conn.cursor()
    sqli = "insert into 35txl values(%s,%s,%s,%s)"  # 35txl为表名
    cur.execute(sqli, (NO, name, tel, shortname))
    cur.close()
    conn.commit()
    conn.close()
    insert_shortname()


def get_shouzimu(hanzi):
    p = Pinyin()
    return p.get_initials(hanzi, u'')


def delete():
    id_todel = raw_input(u"请输入要删除的id：\n")
    conn = init_db()
    cur = conn.cursor()
    row = cur.execute("select * from 35txl")  # 显示这个数据表有多少行

    while (1):
        try:
            int(id_todel)
            break
        except:
            id_todel = raw_input(u"您输入的id不是整数，请输入正确的要删除的id：\n")
    while (1):
        z = int(id_todel)
        if (row + 1 >= z > 0):
            break
        else:
            id_todel = raw_input(u"您输入的id有误，请输入正确的要删除的id：\n")

    sqlscript = "delete from 35txl where id='%s'" % id_todel
    print id_todel
    cur.execute(sqlscript)
    cur.close()
    conn.commit()
    conn.close()


def insert_shortname():  # 一次性产生全部用户的拼音首字母大写
    conn = init_db()
    cur = conn.cursor()
    row = cur.execute("select * from 35txl")  # 显示这个数据表有多少行
    x = db_find_all()
    p = Pinyin()
    sqli = "update 35txl set shortname=%s where id=%s"  # 35txl为表名
    i = 0
    while (i < row):
        shortname = p.get_initials(x[i][1], u'')
        i = i + 1
        cur.execute(sqli, (shortname, i))

    cur.close()
    conn.commit()
    conn.close()


def continue_todo(key):
    print(u"继续本页面的操作请按1，返回请按2，退出请按0\n")
    while (1):
        newkey = raw_input(u"做出你的选择：\n")
        while (1):
            try:
                newkey = int(newkey)
                break
            except:
                newkey = raw_input(u"输入有误，请重新输入\n继续本页面的操作请按1，返回请按2，退出请按0\n做出你的选择：\n")
        if (4 > newkey >= 0):
            break
        else:
            newkey = raw_input(u"你的输入有误，请输入正确的编码（1，2，或0）：\n")
    if (newkey == 1):
        return menu(key)
    elif (newkey == 2):
        return zhuhanshu()
    elif (newkey == 0):
        exit()


def judge_ID(id):  # 判断id是否合法
    conn = init_db()
    cur = conn.cursor()
    row = cur.execute("select * from 35txl")  # 显示这个数据表有多少行
    cur.close()
    conn.commit()
    conn.close()
    z = 0
    try:
        id = int(id)
        if (0 < id <= row):
            z = 1
        else:
            z = 0
            print(u"你输入的id编号非法，请重新输入")
    except:
        print(u"你输入的id编号非法，请重新输入")
    return z


def judge_tel(tel):  # 这个是用来判断是否是11位数的
    z = 0
    try:
        changdu = len(str(int(tel)))  # 计算tel的长度，11位为正常
        tel = int(tel)
        if (changdu == 11):
            z = 1
        else:
            z = 0
            print(u"你输入的tel长度不对，请重新输入z正确的11位数字")
    except:
        print(u"你输入的tel非法，请重新输入")
    return z


def judge_tel2(tel):  # 这个是用来判断是否是数字的
    z = 0;
    try:
        int(tel)
        z = 1
    except:
        print(u"你输入的tel非法，请重新输入")
        z = 0
    return z


def judge_key(key):
    while (1):
        try:
            key = int(key)
            break
        except:
            key = raw_input(u"请输入正确的编码。\n")
    return key


def show_menu():
    print u"请输入要进行的操作"
    print u"1.根据名字查询电话"
    print u"2.根据电话查询名字"
    print u"3.根据名字缩写来查询电话"
    print u"4.显示所有通讯录信息"
    print u"5.添加新的人员通讯信息"
    print u"6.根据id修改电话号码"
    print u"7.根据id修改姓名"
    print u"8.根据id删除数据"
    print u"0.退出"
    print("")


def menu(key):
    if (key == '1'):
        name_to_find = raw_input(u"请输入想要查找的人的姓名：\n")
        find_tel = db_find_row_name(name_to_find)
        while (1):
            if (name_to_find == ''):
                name_to_find = raw_input(u"请不要死命按回车，请输入姓名：\n")
            else:
                break
        chandu = len(find_tel)
        if (chandu != 0):
            print (u"你输入的姓名是%s，根据你提供的信息，我们找到以下信息" % (name_to_find))
            i = 0
            while (i < chandu):
                x1 = find_tel[i]
                x2 = find_tel[i + 1]
                print("%s %s" % (x1, x2))
                i = i + 2
            print(" ")
        else:
            print(u"对不起 没有查询到信息，请确保输入条件正确\n")
            p = raw_input(u"重新查询请按1，返回主菜单请按0,：\n")
            p = judge_key(p)
            p = int(p)
            if (p == 0):
                zhuhanshu()
            else:
                menu('1')
        continue_todo(key)

    elif (key == "2"):
        tel_to_find = raw_input(u"请输入想知道名字的人的电话：\n")
        if (judge_tel2(tel_to_find) == 1):
            find_name = db_find_row_tel(tel_to_find)
        else:
            menu('2')
        while (1):
            if (tel_to_find == ''):
                tel_to_find = raw_input(u"请不要死命按回车，请输入想知道名字的人的电话,：\n")
            else:
                break
        chandu = len(find_name)
        if (chandu != 0):
            print (u"你输入的电话是%s，根据你提供的信息，我们找到以下信息" % (tel_to_find))
            i = 0
            while (i < chandu):
                x1 = find_name[i]
                x2 = find_name[i + 1]
                print("%s %s" % (x1, x2))
                print("")
                i = i + 2
        else:
            print(u"对不起 没有查询到信息，请确保输入条件正确")
            p = raw_input(u"重新查询请按1，返回主菜单请按0,：\n")
            p = int(p)
            p = judge_key(p)
            if (p == 0):
                zhuhanshu()
            else:
                menu('2')
        continue_todo(key)

    elif (key == "3"):
        tel_to_find = raw_input(u"请输入想要查找的人的名字缩写：\n")
        find_tel = db_find_row_sn(tel_to_find)
        while (1):
            if (tel_to_find == ''):
                tel_to_find = raw_input(u"请不要死命按回车，请输入想要查找的人的名字缩写：\n")
            else:
                break
        chandu = len(find_tel)
        if (chandu != 0):
            print (u"你输入的名字缩写是%s，TA的电话是" % (tel_to_find))
            i = 0
            while (i < chandu):
                print(find_tel[i])
                i = i + 1
            print("")
        else:
            print(u"对不起 没有查询到信息，请确保输入条件正确\n")
            p = raw_input(u"重新查询请按1，返回主菜单请按0,：\n")
            p = judge_key(p)
            p = int(p)
            if (p == 0):
                zhuhanshu()
            else:
                menu('2')
        continue_todo(key)

    elif (key == "4"):
        show_all()

    elif (key == "5"):
        NO_toadd = auto_id()
        namel_toadd = raw_input(u"请输入要添加的姓名：\n")
        while (1):
            if (namel_toadd == ''):
                namel_toadd = raw_input(u"请不要死命按回车,请输入姓名：\n")
            else:
                break
        while (1):
            tel_toadd = raw_input(u"请输入要添加电话：...\n")
            if (judge_tel(tel_toadd) == 1):
                break
        while (1):
            if (tel_toadd == ''):
                tel_toadd = raw_input(u"请不要死命按回车,请输入电话：\n")
            else:
                break
        sn_toadd = "suiyi"
        db_insert(NO_toadd, namel_toadd, tel_toadd, sn_toadd)
        continue_todo(key)

    elif (key == "6"):
        NO_toupade = raw_input(u"请输入要修改的编号：\n")
        if (judge_ID(NO_toupade) == 1):
            while (1):
                if (NO_toupade == ''):
                    NO_toupade = raw_input(u"请不要死命按回车,请输入要修改的编号：\n")
                else:
                    break
            tel_toupdate = raw_input(u"请输入要修改的电话：\n")
            if (judge_tel(tel_toupdate) == 0):
                menu('6')
        else:
            menu('6')
        while (1):
            if (tel_toupdate == ''):
                NO_toupade = raw_input(u"请不要死命按回车,请输入要修改的电话：\n")
                if (judge_tel(tel_toupdate) == 0):
                    menu('6')
            else:
                break
        x = db_set_tel(NO_toupade, tel_toupdate)
        if (x == 0):
            print(u"你输入的id号有误，请确认后重试\n")
            return menu('6')
        continue_todo(key)

    elif (key == "7"):
        NO_toupade = raw_input(u"请输入要修改的编号：\n")
        if (judge_ID(NO_toupade) == 1):
            while (1):
                if (NO_toupade == ''):
                    NO_toupade = raw_input(u"请不要死命按回车,请输入要修改的编号：\n")
                else:
                    break
        else:
            menu('7')
        name_toupdate = raw_input(u"请输入要修改的名字：\n")
        while (1):
            if (name_toupdate == ''):
                name_toupdate = raw_input(u"请不要死命按回车,请输入要修改的编号：\n")
            else:
                break
        x = db_set_name(NO_toupade, name_toupdate)
        if (x == 0):
            print(u"你输入的id号有误，请确认后重试\n")
            return menu('7')
        continue_todo(key)

    elif (key == "8"):
        delete()
        print u"删除成功"
        continue_todo(key)

    elif key == "0":
        print(u"欢迎使用汤大哥写的程序，再见")
        exit()

    else:
        print(u"请选择正确的操作\n")
        print ("\n")
        return zhuhanshu()


def zhuhanshu():
    while 1:
        show_menu()
        insert_shortname()  # 时刻刷新首字母拼音
        key1 = raw_input(u"请输入想要做的操作：\n")
        menu(key1)


if __name__ == "__main__":
    zhuhanshu()
