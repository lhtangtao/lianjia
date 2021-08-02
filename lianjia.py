#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#name   = lianjia
#author = rache
#time   = 2017/2/15 21:39
#Description=添加描述信息
#eMail   =tangtao@lhtangtao.com
#git     =lhtangtao
# code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
┏┓      ┏┓
┏┛┻━━━┛┻┓
┃      ☃      ┃
┃  ┳┛  ┗┳  ┃
┃      ┻      ┃
┗━┓      ┏━┛
┃      ┗━━━┓
┃  神兽保佑    ┣┓
┃　永无BUG！   ┏┛
┗┓┓┏━┳┓┏┛
┃┫┫  ┃┫┫
┗┻┛  ┗┻┛
"""
import re
import sys
import urllib2
import time

import datetime
from bs4 import BeautifulSoup
from my_sqldb import insert_info, update_info, get_row, create_table

reload(sys)
sys.setdefaultencoding('utf-8')
current_data = time.strftime('%Y-%m-%d', time.localtime(time.time()))
time.clock()


def get_house_href(total_page=2):
    """
    获取文本后面的链接网址
    :return:无
    """
    i = 1
    while i < total_page:
        url = 'http://hz.lianjia.com/ershoufang/binjiang/pg' + str(i) + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        for title in soup.find_all('div', 'title'):
            print type(title.a)
        i += 1


def get_house(location="binjiang", current_id=1):
    global location_chinese
    current_page = 1  # 当前在第几页
    total_page = 0  # 在这个区里一共有多少页房产信息
    url = 'http://hz.lianjia.com/ershoufang/' + location
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    if location == 'binjiang':
        location_chinese = u'滨江'
    elif location == 'xihu':
        location_chinese = u'西湖'
    elif location == 'qiantangqu':
        location_chinese = u'钱塘区'
    elif location == 'linpingqu':
        location_chinese = u'临平区'
    elif location == 'gongshu':
        location_chinese = u'拱墅'
    elif location == 'shangcheng':
        location_chinese = u'上城'
    elif location == 'yuhang':
        location_chinese = u'余杭'
    elif location == 'xiaoshan':
        location_chinese = u'萧山'
    elif location == 'tonglu1':
        location_chinese = u'桐庐'
    elif location == 'linan':
        location_chinese = u'临安'
    elif location == 'chunan1':
        location_chinese = u'淳安'
    elif location == 'jiande':
        location_chinese = u'建德'
    elif location == 'fuyang':
        location_chinese = u'富阳'
    else:
        print 'wrong location'
    try:
        error = soup.title.text
        if error == u"验证异常流量-链家网":
            print u'ip被封 请尝试更换代理'
            return get_row()
        else:
            pass
    except:
        pass

    for link in soup.find_all('div', 'resultDes clear'):
        context = link.get_text()
        total_house = re.findall(r"\d+\.?\d*", context)[0]  # 总共有多少套房子
        print location + u'一共有' + total_house + u'套房子'
        total_page = int(total_house) / 30 + 1  # 求出一共有多少页
        # total_page=2
    while current_page <= total_page:  # 遍历这个区域的所有房子的信息
        url = 'http://hz.lianjia.com/ershoufang/' + location + '/pg' + str(current_page) + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        ID_num = current_id
        for price in soup.find_all('div', 'totalPrice'):  # 总价的信息
            insert_info("Id", ID_num)
            unit_price = price.get_text()
            unit_price = unit_price[:-1]  # 把最后的一个万字去掉
            update_info('money', unit_price, ID_num)
            update_info('current_data', current_data, ID_num)
            ID_num += 1
        ID_num = current_id

        for positionInfo in soup.find_all('div', 'positionInfo'):
            village = positionInfo.get_text()
            update_info("village", village, ID_num)
            ID_num += 1
        ID_num = current_id

        for link in soup.find_all('div', 'houseInfo'):  # 房子的相关信息，排除出各种别墅
            # print url
            context = link.get_text()
            # print 'info:' + context
            house_type = context.split('|')[0]
            square = context.split('|')[1][:-3]  # 把平米两个字去掉
            orientation = context.split('|')[3]
            if u'别墅' in house_type:
                house_type = context.split('|')[2]
                square = context.split('|')[3][:-3]  # 把平米两个字去掉
                orientation = context.split('|')[4]

            update_info("house_type", house_type, ID_num)
            update_info("square", square, ID_num)
            update_info("orientation", orientation, ID_num)
            update_info("location", location_chinese, ID_num)
            if len(context.split("|")) >= 5:
                decorate = context.split('|')[4]
                update_info("decorate", decorate, ID_num)
            else:
                pass
            ID_num += 1
        ID_num = current_id
        for price in soup.find_all('div', 'unitPrice'):  # 单价的信息
            unit_price = price.get_text()
            # print unit_price
            unit_price = re.findall(r"\d+\.?\d*", unit_price)[0]
            update_info("per_square", unit_price, ID_num)
            update_info("page", current_page, ID_num)
            ID_num += 1
        ID_num = current_id
        for price in soup.find_all("a", attrs={"target": "_blank", 'class': "title"}):  # 获取链接
            url_text = price.get('href')
            # print url_text
            update_info("url", url_text, ID_num)
            ID_num += 1
        current_id = ID_num
        # print current_page
        # print ID_num
        current_page += 1
    return get_row()


if __name__ == '__main__':
    now_time_start = datetime.datetime.now()  # 现在
    localtion_list = ["binjiang", "xihu", "qiantangqu", "linpingqu", "gongshu", "shangcheng", "yuhang", "xiaoshan",
                      "tonglu1", "linan", "chunan1", "jiande", "fuyang"]
    create_table()
    row = get_row()  # 获取数据库中有多少行数据
    for localtion in localtion_list:
        row = get_house(localtion, row + 1)
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print localtion + u'总计已采集数据量为' + str(row) + '    ' + str(time.clock())

    # row = get_house('binjiang', row + 1)
    # print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # print u'总计已采集数据量为' + str(row) + '    ' + str(time.clock())
    # row = get_house("jianggan", row + 1)
    # print u'总计已采集数据量为' + str(row) + '    ' + str(time.clock())
    # row = get_house('gongshu', row + 1)
    # print u'总计已采集数据量为' + str(row) + '    ' + str(time.clock())
    # row = get_house('shangcheng', row + 1)
    # print u'总计已采集数据量为' + str(row) + '    ' + str(time.clock())
    # row = get_house('yuhang', row + 1)
    # print u'总计已采集数据量为' + str(row) + '    ' + str(time.clock())
    # row = get_house('xiaoshan', row + 1)
    # print u'总计已采集数据量为' + str(row) + '    ' + str(time.clock())
    # row = get_house('xihu', row + 1)
    # print u'总计已采集数据量为' + str(row) + '    ' + str(time.clock())
    # row = get_house('xiacheng', row + 1)
    # print u'总计已采集数据量为' + str(row) + '    ' + str(time.clock())
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    now_time_end = datetime.datetime.now()  # 现在
    print (now_time_end - now_time_start)  # 计算时间差
