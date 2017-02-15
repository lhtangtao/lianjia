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

reload(sys)
sys.setdefaultencoding('utf-8')


def get_house_total_price():
    i = 1
    while i < 30:
        url = 'http://hz.lianjia.com/ershoufang/binjiang/pg' + str(i) + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        for price in soup.find_all('div', 'totalPrice'):
            total_price = price.get_text()
            print(total_price)
        i += 1


def get_house_unit_price():
    i = 1
    while i < 30:
        url = 'http://hz.lianjia.com/ershoufang/binjiang/pg' + str(i) + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        for price in soup.find_all('div', 'unitPrice'):
            total_price = price.get_text()
            print re.findall(r"\d+\.?\d*", total_price)[0]
        i += 1


if __name__ == '__main__':
    get_house_unit_price()
