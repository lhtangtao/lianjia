#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#name   = test
#author = tangtao
#time   = 2017/2/15 16:45
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

time.clock()
i = 1
while i < 2:
    url = 'http://hz.lianjia.com/ershoufang/binjiang/pg' + str(i) + '/'
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    # for title in soup.find_all('a'):
    #     total_price = title.get('href')
    #     print(total_price)
    # print (soup.find_all('div', 'total fl'))#获取这个一个页面里有多少houseinfo
    for link in soup.find_all('div', 'houseInfo'):
        context = link.get_text()
        print len(context.split('|'))
    #     unit_price = re.findall(r"\d+\.?\d*", context)[0]
    #     unit_price= int(unit_price)
    #     print unit_price/30
        # village = context.split('|')[4]
        # house_type = context.split('|')[4]
        # print village+house_type
    # for price in soup.find_all('div', 'totalPrice'):
    #     total_price = price.get_text()
    #     print(total_price)
    i += 1

