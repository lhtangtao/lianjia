#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#name   = lianjia
#author = rache
#time   = 2017/2/15 21:39
#Description=添加描述信息
#eMail   =tangtao@lhtangtao.com
#git     =lhtangtao
# code is far away from bugs with the god animal protecting
I love animals. They taste delicious.
┏┓      ┏┓
┏┛┻━━━┛┻┓
┃      ☃      ┃
┃  ┳┛  ┗┳  ┃
┃      ┻      ┃
┗━┓      ┏━┛
┃      ┗━━━┓
┃  神兽保佑    ┣┓
┃　永无BUG！   ┏┛
┗┓┓┏━┳┓┏┛
┃┫┫  ┃┫┫
┗┻┛  ┗┻┛
"""
# from urllib.request import urlopen
import os
import threading
from urllib import urlopen

from bs4 import BeautifulSoup
import urllib2

from cities import get_location, get_sub_location
from lianjia import continue_action


def get_location_sub_relation(city="HZ", exist_file_address="wocao"):
    print city + exist_file_address


if __name__ == '__main__':
    for x in range(5):
        print x
