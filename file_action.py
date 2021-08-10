#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#name=lianjia 
#author=lhtangtao
#time=2021/8/7 17:59
#Mail=tangtao@lhtangtao.com
#git=lhtangtao
#my_website=http://www.lhtangtao.com
#Description=存放文件操作的相关函数
"""
from cities import get_sub_location, get_location
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def write_sub_location(city="hz"):
    """
    把该城市的所有子区域读取出来
    :param city:
    :return:
    """
    file_address = "./city_file/" + city
    open(file_address, "w+")
    list_location = get_location("http://"+city+".lianjia.com/ershoufang/")
    for i in range(len(list_location)):

        url_to_add = list_location[i].split("=")[1]
        print url_to_add
        url = "https://" + city + ".lianjia.com" + url_to_add
        print url
        try:
            for j in range(len(get_sub_location(url))):
                x = get_sub_location(url)[j]
                print x
                test = open(file_address, "a+")
                test.write(x + '\n')
        except:
            print list_location[i] + u"这个区没有数据"


if __name__ == '__main__':
    write_sub_location("nb")
