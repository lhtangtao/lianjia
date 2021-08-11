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
    list_location = get_location("http://" + city + ".lianjia.com/ershoufang/")
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
    clear(city)


def read_sub_location(city="HZ"):
    list_dst = []
    file_address = "./city_file/" + city
    for line in open(file_address):
        list_dst.append(line.split("=")[1].replace("\n", ""))
    return list_dst


def clear(city="NB"):
    """
    文件夹去重
    :param city:
    :return:
    """
    file_list = []
    file_address = "./city_file/" + city
    with open(file_address, "r") as f:
        file_2 = f.readlines()
        for file in file_2:
            file_list.append(file)
        out_file1 = set(file_list)  # set()函数可以自动过滤掉重复元素
        last_out_file = list(out_file1)
        open(file_address, "w")
        for out in last_out_file:
            with open(file_address, "a+") as f:  # 去重后文件写入文件里
                f.write(out)


if __name__ == '__main__':
    write_sub_location("HZ")
    # clear("NB")

    # print read_sub_location()[1]
