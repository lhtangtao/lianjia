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
import os

reload(sys)
sys.setdefaultencoding('utf8')
denominator = 20


def get_all_cities():
    all_cities = []
    if os.path.exists("./city_file/all"):
        for line in open("./city_file/all"):
            all_cities.append(line.replace("\n", ""))
    else:
        pass
    return all_cities


def write_sub_location(city="HZ"):
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
    return spilt_file(city)


def read_sub_location(file_address="./city_file/" + "HZ"):
    list_dst = []
    if os.path.exists(file_address):
        for line in open(file_address):
            list_dst.append(line.split("=")[1].replace("\n", ""))
    else:
        pass
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


def delete_file_line(city="HZ", sub_location="ershoufang/daxuechengbei/"):
    for i in range(10):
        file_address = "./city_file/" + city + str(i)
        if os.path.exists(file_address):
            with open(file_address, "r") as f:
                lines = f.readlines()
            with open(file_address, "w") as f_w:
                for line in lines:
                    if sub_location in line:
                        continue
                    f_w.write(line)
    print u"delete " + sub_location + u"success"


def delete_file(file_address):
    os.remove(file_address)


def spilt_file(city="HZ"):
    file_address = "./city_file/" + city
    count = 0
    f = open(file_address, "r")
    for line in f.readlines():
        count = count + 1
        file_address = "./city_file/" + city + str(count / denominator)
        test = open(file_address, "a+")
        test.write(line)
    if os.path.exists("./city_file/" + city + "1"):
        os.remove("./city_file/" + city)
    else:
        os.remove("./city_file/" + city + "0")
    return count


if __name__ == '__main__':
    print get_all_cities()
