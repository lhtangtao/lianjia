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

#
# html = urlopen("http://pubg.ali213.net/pubg10/overview?nickname=yyf1234")
# bs0bj = BeautifulSoup(html, "html.parser")
#
# nums = bs0bj.find(class_="container").find(class_="opc-bg").find(class_="typeBtns-cont").find(
#     class_="items-bar clearfix")
# print(nums)

if __name__ == '__main__':
    test = open("./city_file/NB","r")
    print test.read(10)
    test.close()


