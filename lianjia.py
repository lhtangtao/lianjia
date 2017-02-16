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
import urllib2
import re
import sys
import urllib2
import time
from bs4 import BeautifulSoup

from my_sqldb import insert_info, update_info

reload(sys)
sys.setdefaultencoding('utf-8')
total_page = 2
current_data = time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_house_href():
    """
    获取文本后面的链接网址
    :return:
    """
    i = 1
    while i < total_page:
        url = 'http://hz.lianjia.com/ershoufang/binjiang/pg' + str(i) + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        for title in soup.find_all('div', 'title'):
            print type(title.a)
        i += 1


def get_house():
    ID_num = 0
    i = 1
    while i < total_page:
        url = 'http://hz.lianjia.com/ershoufang/binjiang/pg' + str(i) + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        for price in soup.find_all('div', 'totalPrice'):
            ID_num += 1
            insert_info("Id", ID_num)
            total_price = price.get_text()
            update_info('money', total_price, ID_num)
            update_info('current_data', current_data, ID_num)
        ID_num = 0
        for link in soup.find_all('div', 'houseInfo'):
            ID_num += 1
            context = link.get_text()
            village = context.split('|')[0]
            house_type = context.split('|')[1]
            square = context.split('|')[2]
            orientation = context.split('|')[3]
            decorate = context.split('|')[4]
            update_info("village", village, ID_num)
            update_info("house_type", house_type, ID_num)
            update_info("square", square, ID_num)
            update_info("orientation", orientation, ID_num)
            update_info("decorate", decorate, ID_num)
        ID_num = 0
        for price in soup.find_all('div', 'unitPrice'):
            ID_num += 1
            total_price = price.get_text()
            unit_price = re.findall(r"\d+\.?\d*", total_price)[0]
            update_info("per_square", unit_price, ID_num)
        i += 1


if __name__ == '__main__':
    get_house()
