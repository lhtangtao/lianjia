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
import random
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
        soup = BeautifulSoup(page, "html.parser")
        for title in soup.find_all('div', 'title'):
            print type(title.a)
        i += 1


def get_house(location="binjiang", current_id=1):
    current_page = 1
    total_page = 2
    while current_page < total_page or current_page == total_page:
        url = 'http://hz.lianjia.com/ershoufang/' + location + '/pg' + str(current_page) + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        # print soup
        ID_num = current_id
        i = 1
        print soup.find_all("a", attrs={"target": "_blank", 'class': 'title', 'data-el': "ershoufang"})
        for price in soup.find_all("a", attrs={"target": "_blank", 'class':'title','data-el': "ershoufang"}):  # 获取链接
            url_text = price.get('href')
            print str(ID_num) +"   "+str(i)+ "   "+url_text
            update_info("url", url_text, ID_num)
            ID_num += 1
            i += 1
        current_id = ID_num
    return get_row()


if __name__ == '__main__':
    create_table()
    row = get_row()  # 获取数据库中有多少行数据
    print row
    # row = get_house('xihu', row + 1)
    # print row
    # row = get_house('xiacheng', row + 1)
    # print row
    row = get_house('binjiang', row + 1)
    # print row
    # row = get_house("jianggan", row + 1)
    # print row
    # row = get_house('gongshu', row + 1)
    # print row
    # row = get_house('shangcheng', row + 1)
    # print row
    # row = get_house('yuhang', row + 1)
    # print row
    # row = get_house('xiaoshan', row + 1)
    # print row
    print(time.clock())
