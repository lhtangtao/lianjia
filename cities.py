#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
#name=lianjia 
#author=lhtangtao
#time=2021/8/7 09:31
#Mail=tangtao@lhtangtao.com
#git=lhtangtao
#my_website=http://www.lhtangtao.com
#Description=存放城市相关转换信息
"""

import sys
import time
import urllib2

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")


def get_city_divisions(city="HZ"):
    """
    获取该城市下所有行政区的信息，写到文件中
    :param city:
    :return:
    """
    url = "https://" + city + "hz.lianjia.com/ershoufang/rs/"


def get_city_name(city="HZ"):
    if city == "HZ":
        return u'杭州'
    if city == "NB":
        return u"宁波"
    if city == "quanzhou":
        return u"泉州"
    if city == "WZ":
        return u"温州"
    if city == "taizhou":
        return u"台州"
    if city == "SX":
        return u"绍兴"
    if city == "huzhou":
        return u"湖州"
    if city == "JX":
        return u"嘉兴"
    if city == "JH":
        return u"金华"
    if city == "quzhou":
        return u"衢州"
    if city == "QD":
        return u"青岛"
    if city == "WH":
        return u"武汉"


def get_location(url="http://hz.lianjia.com/ershoufang/"):
    """
    输入url后获取当前城市的区县信息及后面的链接
    :param url:
    :return:杭州大江东在售二手房 =/ershoufang/dajiangdong1/
    """
    list_location_divisions = []
    while True:
        req = urllib2.Request(url)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
        try:
            error = soup.title.text
            if error == u"验证异常流量-链家网":
                print u'ip被封 重启吧'
                time.sleep(600)
            elif error == u"人机认证":
                print u'ip被封 重启吧'
                time.sleep(600)
            else:
                break
        except:
            pass

    for link in soup.find_all("div", attrs={'data-role': "ershoufang"}):
        location_souce = link.find_all("div")[0]
        for location in location_souce.find_all("a"):
            list_location_divisions.append(location.get("title") + "=" + location.get("href"))
    return list_location_divisions


def get_sub_location(url="https://nb.lianjia.com/ershoufang/haishuqu1/"):
    global location_souce
    list_sub_location = []
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    for link in soup.find_all("div", attrs={'data-role': "ershoufang"}):
        location_souce = link.find_all("div")[0]
        sub_location_source = link.find_all("div")[1]
        for sub_location in sub_location_source.find_all("a"):
            list_sub_location.append(sub_location.text + "=" + sub_location.get("href"))
    return list_sub_location


def get_true_location_by_sub():
    """
    通过传入子区域，获取他所在的真正行政区域
    建议半年执行一次 最近执行是2021年11月18日
    :param url:
    :return:
    """
    from file_action import get_all_cities
    cities_list = get_all_cities()
    for city_to in cities_list:
        city_name = get_city_name(city_to)
        print u"开始采集这个城市的数据了" + city_name
        file_address = "./city_file_backup/" + city_to
        test = open(file_address, "r+")
        for line in test:
            sub_location_url_to_add = line.split("=")[1]
            url = "https://" + city_to + ".lianjia.com" + sub_location_url_to_add
            req = urllib2.Request(url)
            page = urllib2.urlopen(req)
            soup = BeautifulSoup(page, "html.parser")
            list_temp = []
            for link in soup.find_all("a", attrs={'class': "selected"}):
                list_temp.append(link.get_text().split("\n")[0])
            file_address = "./relation"
            test = open(file_address, "a+")
            test.write(city_name + "-" + list_temp[1] + "-" + list_temp[2] + "-" + sub_location_url_to_add)


if __name__ == '__main__':
    print get_location()[1]

