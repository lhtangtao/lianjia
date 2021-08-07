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
