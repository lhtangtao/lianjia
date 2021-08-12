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
import urllib2
from bs4 import BeautifulSoup


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


def get_location(url="http://hz.lianjia.com/ershoufang/"):
    """
    输入url后获取当前城市的区县信息及后面的链接
    :param url:
    :return:杭州大江东在售二手房 =/ershoufang/dajiangdong1/
    """
    list_location_divisions = []
    req = urllib2.Request(url)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
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


if __name__ == '__main__':
    get_city_divisions()
