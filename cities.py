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


def city_region(city="HZ", location="binjiang"):
    location_chinese_from_region = ""
    if city == "HZ":
        if location == 'binjiang':
            location_chinese_from_region = u'滨江区'
        elif location == 'xihu':
            location_chinese_from_region = u'西湖区'
        elif location == 'qiantangqu':
            location_chinese_from_region = u'钱塘区'
        elif location == 'linpingqu':
            location_chinese_from_region = u'临平区'
        elif location == 'gongshu':
            location_chinese_from_region = u'拱墅区'
        elif location == 'shangcheng':
            location_chinese_from_region = u'上城区'
        elif location == 'yuhang':
            location_chinese_from_region = u'余杭区'
        elif location == 'xiaoshan':
            location_chinese_from_region = u'萧山区'
        elif location == 'tonglu1':
            location_chinese_from_region = u'桐庐区'
        elif location == 'linan':
            location_chinese_from_region = u'临安区'
        elif location == 'chunan1':
            location_chinese_from_region = u'淳安县'
        elif location == 'jiande':
            location_chinese_from_region = u'建德市'
        elif location == 'fuyang':
            location_chinese_from_region = u'富阳区'
        else:
            print 'wrong location'
    if city == "NB":
        if location == "haishuqu1":
            location_chinese_from_region = u"海曙区"
        elif location == "jiangbeiqu1":
            location_chinese_from_region = u"江北区"
        elif location == "zhenhaiqu1":
            location_chinese_from_region = u"镇海区"
        elif location == "beilunqu1":
            location_chinese_from_region = u"北仑区"
        elif location == "yinzhouqu2":
            location_chinese_from_region = u"鄞州区"
        elif location == "yuyaoshi":
            location_chinese_from_region = u"余姚市"
        elif location == "cixishi":
            location_chinese_from_region = u"慈溪市"
        elif location == "fenghuaqu":
            location_chinese_from_region = u"奉化区"
        elif location == "xiangshanxian":
            location_chinese_from_region = u"象山县"
        elif location == "ninghaixian":
            location_chinese_from_region = u"宁海县"
        elif location == "hangzhouwanxinqu1":
            location_chinese_from_region = u"杭州湾新区"
        else:
            print "wrong location"

    return location_chinese_from_region


def get_city_name(city="HZ"):
    if city == "HZ":
        return u'杭州'
    if city == "NB":
        return u"宁波"


def get_location(url="http://hz.lianjia.com/ershoufang/"):
    """
    输入url后获取当前城市的区县信息及后面的链接
    :param url:
    :return:杭州大江东在售二手房 =/ershoufang/dajiangdong1/
    """
    list_location = []
    req = urllib2.Request(url)
    # req = urllib2.Request("http://nb.lianjia.com/ershoufang/haishuqu1/pg1/")
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    for link in soup.find_all("div", attrs={'data-role': "ershoufang"}):
        location_souce = link.find_all("div")[0]
        for location in location_souce.find_all("a"):
            list_location.append(location.get("title") + "=" + location.get("href"))
    return list_location


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
    list_location = get_location()
    for i in range(len(list_location)):
        url_to_add = list_location[i].split("=")[1]
        url = "https://hz" + ".lianjia.com" + url_to_add
        print url
        try:
            for i in range(len(get_sub_location(url))):
                print get_sub_location(url)[i]
        except:
            print u"这个区没有数据"

