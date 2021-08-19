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
from urllib import urlopen

from bs4 import BeautifulSoup
import urllib2

if __name__ == '__main__':
    village = u" 延安三路10-12、16-28（双号）    -  北仲 "
    x = ""
    # village = u"利津路32-40（双号）    -  海泊河 "
    if len(village.split("-")) > 2:
        village = village.replace(" ", "")
        print village
        for i in range(len(village.split("-"))-1):
            print village.split("-")[i]
            x = x + village.split("-")[i]
    print x
