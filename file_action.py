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
    把该城市的所有子区域读取出来存放到一个文件
    :param city:
    :return:
    """
    file_address = "./city_file/" + city
    open(file_address, "w+")
    list_location = get_location("http://" + city + ".lianjia.com/ershoufang/")
    if len(list_location) > 150:
        print u"*************sub_location已经超过150个了 请注意修改代码**************"
    for i in range(len(list_location)):
        url_to_add = list_location[i].split("=")[1]
        print url_to_add
        url = "https://" + city + ".lianjia.com" + url_to_add
        print url
        try:
            for j in range(len(get_sub_location(url))):
                sub_location_url = get_sub_location(url)[j]
                test = open(file_address, "a+")
                test.write(sub_location_url + '\n')
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
    # z = 1
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
            #     if z % 25 == 0:
            #         f.write("\n")
            # z = z + 1


def delete_file(city="HZ", sub_location="ershoufang/jiulian/"):
    file_address = "./city_file/" + city
    with open(file_address, "r") as f:
        lines = f.readlines()
    with open(file_address, "w") as f_w:
        for line in lines:
            if sub_location in line:
                continue
            f_w.write(line)
    print u"delete "+sub_location+u"success"


if __name__ == '__main__':
    delete_file("HZ","sandun")
    # clear("NB")

    # print read_sub_location()[1]
