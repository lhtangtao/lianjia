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
from cities import get_city_name, get_sub_location
from file_action import read_sub_location, write_sub_location

reload(sys)
sys.setdefaultencoding('utf-8')
current_data = time.strftime('%Y-%m-%d', time.localtime(time.time()))
time.clock()


def continue_action():
    while True:
        source = raw_input(u"请输入任意键后按回车继续")
        if source != "111111":
            break
    print u"已解除封印，可继续执行"


def get_house(city="quanzhou", sub_location="baolongguangchang", current_id=1):
    current_page = 1  # 当前在第几页
    total_page = 0  # 在这个区里一共有多少页房产信息
    url_source = "http://" + city + ".lianjia.com" + sub_location
    req = urllib2.Request(url_source)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    try:
        error = soup.title.text
        if error == u"验证异常流量-链家网":
            print u'ip被封 请尝试更换代理'
            continue_action()
        elif error == u"人机认证":
            print u'ip被封 请尝试更换代理'
            continue_action()
        else:
            pass
    except:
        pass

    for link in soup.find_all('div', 'resultDes clear'):
        context = link.get_text()
        # print context #示例是   共找到 3435 套滨江二手房with(document)write('<a href="/ershoufang/"><span></span>清空条件</a>');保存搜索
        total_house = re.findall(r"\d+\.?\d*", context)[0]  # 总共有多少套房子
        print sub_location + u'一共有' + total_house + u'套房子'
        total_page = int(total_house) / 30 + 1  # 求出一共有多少页
        if total_page > 100:
            total_page = 100
        print total_page
    while current_page <= total_page:  # 遍历这个区域的所有房子的信息
        url = url_source + '/pg' + str(current_page) + '/'
        print url
        page = urllib2.urlopen(url)
        try:
            soup = BeautifulSoup(page, "html.parser")
        except:
            print url
            print soup
        list_temp = []
        for link in soup.find_all("a", attrs={'class': "selected"}):
            list_temp.append(link.get_text().split("\n")[0])
        location_chinese = list_temp[1]
        ID_num = current_id
        city_name = get_city_name(city)
        for price in soup.find_all('div', 'totalPrice'):  # 总价的信息
            insert_info("Id", ID_num)
            unit_price = price.get_text()
            unit_price = unit_price[:-1]  # 把最后的一个万字去掉
            update_info('money', unit_price, ID_num)
            update_info('current_data', current_data, ID_num)
            update_info('city', city_name, ID_num)
            ID_num += 1
        ID_num = current_id

        for positionInfo in soup.find_all('div', 'positionInfo'):
            village = positionInfo.get_text()
            sub_location = village.split('-')[1].strip()
            village = village.split('-')[0].strip()
            update_info("village", village, ID_num)
            update_info("sub_location", sub_location, ID_num)
            ID_num += 1
        ID_num = current_id

        for link in soup.find_all('div', 'houseInfo'):  # 房子的相关信息，排除出各种别墅
            context = link.get_text()
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
        current_page += 1
    return get_row()


def gather(city="HZ"):
    now_time_start_all = datetime.datetime.now()  # 现在
    # write_sub_location(city)  # 把该城市下的二级区域获取
    localtion_list = read_sub_location(city)
    row = get_row()  # 获取数据库中有多少行数据
    for sub_localtion in localtion_list:
        now_time_start = datetime.datetime.now()  # 现在
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        row = get_house(city, sub_localtion, row + 1)
        now_time_end = datetime.datetime.now()  # 现在
        print sub_localtion + u'已采集完毕，总计已采集数据量为' + str(row) + '    ' + str((now_time_end - now_time_start))
        print u"强制等待半分钟"
        time.sleep(10 * 1)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    now_time_end = datetime.datetime.now()  # 现在
    print (now_time_end - now_time_start_all)  # 计算时间差


if __name__ == '__main__':
    create_table()
    # gather("quanzhou")
    gather("NB")

    # get_sub_location()
