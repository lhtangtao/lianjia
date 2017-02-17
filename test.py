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

from my_sqldb import insert_info, update_info, get_row, create_table

reload(sys)
sys.setdefaultencoding('utf-8')

current_data = time.strftime('%Y-%m-%d', time.localtime(time.time()))
time.clock()


def get_house_href(total_page=2):
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


def get_house(location="binjiang", current_id=1):
    current_page = 1
    url = 'http://hz.lianjia.com/ershoufang/' + location
    url = 'http://hz.lianjia.com/ershoufang/' + location + '/pg' + str(current_page) + '/'
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    # print soup.find_all("div","title")
    for price in soup.find_all("a", attrs={"target": "_blank", 'class': "title"}):
        print price.get('href')
    return get_row()


if __name__ == '__main__':
    create_table()
    row = get_row()  # 获取数据库中有多少行数据
    # row = get_house('xihu', row + 1)
    # row = get_house('xiacheng', row + 1)
    # row = get_house('binjiang', row + 1)
    # row = get_house("jianggan", row + 1)
    # row = get_house('gongshu', row + 1)
    # row = get_house('shangcheng', row + 1)
    row = get_house('yuhang', row + 1)
    row = get_house('xiaoshan', row + 1)
    print(time.clock())
