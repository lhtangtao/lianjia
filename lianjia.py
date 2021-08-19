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
from my_sqldb import get_row, create_table, insert_info
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


def get_house(city="quanzhou", sub_location="baolongguangchang"):
    global city_name, location_chinese, j
    current_page = 1  # 当前在第几页
    total_page = 0  # 在这个区里一共有多少页房产信息
    url_source = "http://" + city + ".lianjia.com" + sub_location
    while True:
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
                break
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
    while current_page <= total_page:  # 遍历这个区域的所有房子的信息
        url = url_source + 'pg' + str(current_page) + '/'
        page = urllib2.urlopen(url)
        print url
        try:
            soup = BeautifulSoup(page, "html.parser")
        except:
            print url
            print soup
        if current_page == 1:  # 第一页和最后一页 location_chinese的名字都是一样的
            list_temp = []
            for link in soup.find_all("a", attrs={'class': "selected"}):
                list_temp.append(link.get_text().split("\n")[0])
            location_chinese = list_temp[1]
            city_name = get_city_name(city)  # 第一页和最后一页 city_name的名字都是一样的
        list_village = []
        list_sub_location = []
        for positionInfo in soup.find_all('div', 'positionInfo'):
            village = positionInfo.get_text()
            village_new = ""
            if len(village.split("-")) > 2:
                village = village.replace(" ", "")
                print village
                for i in range(len(village.split("-")) - 1):
                    print village.split("-")[i]
                    village_new = village_new + village.split("-")[i]
                village = village_new

            else:
                sub_location = village.split('-')[1].strip()
                village = village.split('-')[0].strip()
            list_village.append(village)
            list_sub_location.append(sub_location)

        list_house_type = []
        list_square = []
        list_orientation = []
        list_decorate = []
        for link in soup.find_all('div', 'houseInfo'):  # 房子的相关信息，排除出各种别墅
            context = link.get_text()
            house_type = context.split('|')[0]
            square = context.split('|')[1][:-3]  # 把平米两个字去掉
            orientation = context.split('|')[3]
            if u'别墅' in house_type:
                house_type = context.split('|')[2]
                square = context.split('|')[3][:-3]  # 把平米两个字去掉
                orientation = context.split('|')[4]
            if len(context.split("|")) >= 5:
                decorate = context.split('|')[4]
            else:
                decorate = " "
            list_decorate.append(decorate)
            list_house_type.append(house_type)
            list_square.append(square)
            list_orientation.append(orientation)
        list_money = []
        i = 0
        list_temp = []
        for price in soup.find_all('div', 'totalPrice'):  # 总价的信息
            if u"暂无价格" in price.get_text():
                money = " "
                list_temp.append(i)
            else:
                money = price.get_text()
                money = money[:-1]  # 把最后的一个万字去掉
            i = i + 1
            list_money.append(money)
        list_per_square = []

        for price in soup.find_all('div', 'unitPrice'):  # 单价的信息
            per_square = price.get_text()
            per_square = re.findall(r"\d+\.?\d*", per_square)[0]
            list_per_square.append(per_square)
        for j in range(len(list_temp)):
            list_per_square.insert(list_temp[j], " ")

        list_url_text = []
        for price in soup.find_all("a", attrs={"target": "_blank", 'class': "title"}):  # 获取链接
            url_text = price.get('href')
            list_url_text.append(url_text)
        for i in range(len(list_money)):
            insert_info(
                '"' + current_data + '","' + city_name + '","' + location_chinese + '","' + sub_location + '","' +
                list_village[
                    i] + '","' + list_house_type[
                    i] + '","' + list_square[i] + '","' + list_orientation[i] + '","' + list_decorate[i] + '","' +
                list_money[
                    i] + '","' + list_per_square[i] + '","' + list_url_text[i] + '","' + str(current_page) + '"')
        current_page += 1
    return get_row()


def gather(city="HZ"):
    now_time_start_all = datetime.datetime.now()  # 现在
    # write_sub_location(city)  # 把该城市下的二级区域获取
    localtion_list = read_sub_location(city)
    for sub_localtion in localtion_list:
        now_time_start = datetime.datetime.now()  # 现在
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        row = get_house(city, sub_localtion)
        now_time_end = datetime.datetime.now()  # 现在
        print sub_localtion + u'已采集完毕，总计已采集数据量为' + str(row) + '    ' + str((now_time_end - now_time_start))
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print u"强制等待10秒"
        time.sleep(20 * 1)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    now_time_end = datetime.datetime.now()  # 现在
    print (now_time_end - now_time_start_all)  # 计算时间差


if __name__ == '__main__':
    create_table(False)
    gather("QD")
