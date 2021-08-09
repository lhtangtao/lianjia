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
from cities import get_sub_location

def write_file(path, text):
    test = open(path, "w+")
    test.write(text + '\n')
    test.close()


if __name__ == '__main__':
    print get_sub_location()
    write_file("./city_file/NB", "wwwwwww")
