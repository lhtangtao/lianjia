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

# Some User Agents
hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
       {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}, \
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}, \
       {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'}, \
       {
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}, \
       {
           'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}, \
       {
           'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}, \
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'}, \
       {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}, \
       {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}, \
       {
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}, \
       {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'}, \
       {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

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
    req = urllib2.Request(url, headers=hds[random.randint(0, len(hds) - 1)])
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "lxml")
    print soup
    if location == 'binjiang':
        location_chinese = u'滨江'
    elif location == 'xihu':
        location_chinese = u'西湖'
    elif location == 'xiacheng':
        location_chinese = u'下城'
    elif location == 'jianggan':
        location_chinese = u'江干'
    elif location == 'gongshu':
        location_chinese = u'拱墅'
    elif location == 'shangcheng':
        location_chinese = u'上城'
    elif location == 'yuhang':
        location_chinese = u'余杭'
    elif location == 'xiaoshan':
        location_chinese = u'萧山'
    else:
        print 'wrong location'
    for link in soup.find_all('div', 'resultDes clear'):
        context = link.get_text()
        total_house = re.findall(r"\d+\.?\d*", context)[0]  # 总共有多少套房子
        print location + u'一共有' + total_house + u'套房子'
        total_page = int(total_house) / 30 + 1  # 求出一共有多少页
    while current_page < total_page or current_page == total_page:
        url = 'http://hz.lianjia.com/ershoufang/' + location + '/pg' + str(current_page) + '/'
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        # print soup
        ID_num = current_id
        for price in soup.find_all('div', 'totalPrice'):
            insert_info("Id", ID_num)
            total_price = price.get_text()
            update_info('money', total_price, ID_num)
            update_info('current_data', current_data, ID_num)
            ID_num += 1
        ID_num = current_id
        for link in soup.find_all('div', 'houseInfo'):
            # print url
            context = link.get_text()
            village = context.split('|')[0]
            house_type = context.split('|')[1]
            square = context.split('|')[2]
            orientation = context.split('|')[3]
            if u'别墅' in house_type:
                house_type = context.split('|')[2]
                square = context.split('|')[3]
                orientation = context.split('|')[4]
            update_info("village", village, ID_num)
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
        for price in soup.find_all('div', 'unitPrice'):
            total_price = price.get_text()
            unit_price = re.findall(r"\d+\.?\d*", total_price)[0]
            update_info("per_square", unit_price, ID_num)
            update_info("page", current_page, ID_num)
            ID_num += 1
        ID_num = current_id
        for price in soup.find_all("a", attrs={"target": "_blank", 'class': "title"}):
            url_text = price.get('href')
            update_info("url", url_text, ID_num)
            ID_num += 1
        current_id = ID_num
        print current_page
        print ID_num
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
