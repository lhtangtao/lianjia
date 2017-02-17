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
# Some User Agents
hds = [
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    { 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}, \
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}
]


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
    total_page = 2
    while current_page < total_page or current_page == total_page:
        url = 'http://hz.lianjia.com/ershoufang/' + location + '/pg' + str(current_page) + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        # print soup
        ID_num = current_id
        for link in soup.find_all('div', 'houseInfo'):
            # print url
            context = link.get_text()
            print context
            # print u'changdu' + str(len(context.split("|")))
            village = context.split('|')[0]
            house_type = context.split('|')[1]
            square = context.split('|')[2]
            orientation = context.split('|')[3]
            if u'别墅'in house_type:
                print 'hahahahahaha'

                house_type=context.split('|')[2]
                square= context.split('|')[3]
                orientation=context.split('|')[4]
                print house_type+square+orientation
            if len(context.split("|")) >= 5:
                decorate = context.split('|')[4]
                update_info("decorate", decorate, ID_num)
            else:
                pass
            ID_num += 1
        current_page += 1
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
