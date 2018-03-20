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
import sys

import time
from selenium import webdriver

from my_sqldb import create_table

reload(sys)
sys.setdefaultencoding('utf-8')


def do_js():
    driver = webdriver.Chrome()
    driver.get('http://im.qq.com/download/')
    js = """a = 5;
    b = 6;
    c = a + b;
    return c;
    """
    return driver.execute_script(js)


if __name__ == '__main__':
    # print do_js()
    create_table()
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
