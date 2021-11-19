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
import time

from cities import get_sub_location, get_location
import sys
import os
import shutil

reload(sys)
sys.setdefaultencoding('utf8')


def get_all_cities_to_collect():
    """
    这个是获取要抓的城市的链接用的  每个月第一次跑 这个地方的数据肯定是空的
    :return:
    """
    all_cities = []
    if os.path.exists("./city_file/all"):
        for line in open("./city_file/all"):
            count = 0
            for i in range(10):
                if os.path.exists("./city_file/" + line.replace("\n", "") + str(i)) or os.path.exists(
                        "./city_file/" + line.replace("\n", "")):
                    count = count + 1
            if count != 0:
                all_cities.append(line.replace("\n", ""))
    else:
        print u"all"
    return sorted(all_cities, key=str.lower)


def get_all_cities():
    """
    返回的列表如下所示
    ['HZ', 'JX', 'huzhou', 'NB', 'SX', 'JH', 'WZ', 'taizhou', 'quzhou', 'quanzhou', 'QD', 'WH']
    :return:
    """
    all_cities = []
    if os.path.exists("./city_file/all"):
        for line in open("./city_file/all"):
            all_cities.append(line.replace("\n", ""))
    else:
        pass
    return all_cities


def write_sub_location(city="JH"):
    """
    把该城市的所有子区域读取出来存放到一个文件
    :param city:
    :return:
    """
    if not os.path.exists("./city_file_backup/"):
        os.mkdir("./city_file_backup/")
    file_address = "./city_file_backup/" + city
    open(file_address, "w+")
    list_location = get_location("http://" + city + ".lianjia.com/ershoufang/")
    if len(list_location) > 150:
        print u"*************sub_location已经超过150个了 请注意修改代码**************"
    for i in range(len(list_location)):
        url_to_add = list_location[i].split("=")[1]
        url = "https://" + city + ".lianjia.com" + url_to_add
        print url + u"开始采集写入到文件夹中"
        try:
            for j in range(len(get_sub_location(url))):
                sub_location_url = get_sub_location(url)[j]
                print url_to_add + u"的sub_location_url" + "is" + sub_location_url
                test = open(file_address, "a+")
                test.write(sub_location_url + '\n')
            print url + u"的信息已写入到文件夹中"
        except:
            print list_location[i] + u"这个区没有数据"
    clear(city)
    # return spilt_file(city)


def read_sub_location(file_address="./city_file/" + "HZ0"):
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
    print u"开始文件夹去重工作  文件名为" + city
    file_list = []
    file_address = "./city_file_backup/" + city
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


def spilt_file(city="HZ", copy=False):
    print u"开始切割文件 名字为"
    if copy:
        file_address = "./city_file/" + city
        shutil.copy(file_address, "./city_file_backup")
    else:
        file_address = "./city_file_backup/" + city
    denominator = len(open(file_address).readlines()) / 5
    count = 0
    f = open(file_address, "r")
    for i in range(10):
        if os.path.exists("./city_file/" + city + str(i)):
            open("./city_file/" + city + str(i), "w+")
    for line in f.readlines():
        count = count + 1
        file_address = "./city_file/" + city + str(count / denominator)
        test = open(file_address, "a+")
        test.write(line)
    print u"文件切割完毕"
    return count


def spilt_file_all():
    """
    step 2
    获取完城市数据后全部进行切割
    :return:
    """
    for city in get_all_cities():
        spilt_file(city)


def write_sub_location_all():
    for city in get_all_cities():
        write_sub_location(city)


if __name__ == '__main__':
    print spilt_file_all()
