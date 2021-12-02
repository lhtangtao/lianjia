#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
import urllib2

from bs4 import BeautifulSoup
from file_action import get_all_cities
from cities import get_city_name, get_location
from my_sqldb import init_db, insert_city, insert_sub_location, insert_location

current_data = time.strftime('%Y-%m', time.localtime(time.time()))


def get_real_city_count(city="HZ", date="2021-11"):
    """
    输入城市 去查db 获取这个城市在该月份所采集的数量
    :param city:
    :param date:
    :return:
    """
    conn = init_db()
    cur = conn.cursor()
    city = get_city_name(city)
    sql_script0 = 'SELECT COUNT(*) FROM lianjia WHERE date = "'
    sql_script1 = '"  and city ="'
    sql_script = sql_script0 + date + sql_script1 + city + '"'
    cur.execute(sql_script)
    return cur.fetchone()[0]


def get_real_location_count(location="钱塘区", date="2021-11"):
    """
    输入城市 去查db 获取这个行政区在该月份所采集的数量
    :param location:
    :param date:
    :return:
    """
    conn = init_db()
    cur = conn.cursor()
    sql_script0 = 'SELECT COUNT(*) FROM lianjia WHERE date = "'
    sql_script1 = '"  and location ="'
    sql_script = sql_script0 + date + sql_script1 + location + '"'
    cur.execute(sql_script)
    return cur.fetchone()[0]


def get_real_sub_location_count(sub_location="良渚", date="2021-11"):
    """
    输入城市 去查db 获取这个行政区在该月份所采集的数量
    :param sub_location:
    :param date:
    :return:
    """
    conn = init_db()
    cur = conn.cursor()
    sql_script0 = 'SELECT COUNT(*) FROM lianjia WHERE date = "'
    sql_script1 = '"  and sub_location ="'
    sql_script = sql_script0 + date + sql_script1 + sub_location + '"'
    cur.execute(sql_script)
    return cur.fetchone()[0]


def get_expect_city_count(city="hz"):
    """
    输入城市 去查db 获取这个城市在该月份网页中展示的数量
    :param city:
    :return:
    """
    url = "http://" + city + ".lianjia.com/ershoufang"
    count_in_page = 0
    while True:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        error = soup.title.text
        if error == u"验证异常流量-链家网" or error == u"人机认证":
            count_in_page = count_in_page + 1
            time.sleep(600)
        else:
            break
    for link in soup.find_all('div', 'resultDes clear'):
        context = link.get_text()
        total_house = re.findall(r"\d+\.?\d*", context)[0]  # 总共有多少套房子
        return total_house


def get_expect_location_count(city="huzhou", location="/ershoufang/nanxunqu/"):
    url = "http://" + city + ".lianjia.com" + location
    count_in_page = 0
    while True:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        error = soup.title.text
        if error == u"验证异常流量-链家网" or error == u"人机认证":
            count_in_page = count_in_page + 1
            time.sleep(600)
        else:
            break
    for link in soup.find_all('div', 'resultDes clear'):
        context = link.get_text()
        total_house = re.findall(r"\d+\.?\d*", context)[0]  # 总共有多少套房子
        return total_house


def statistics_city():
    for i in get_all_cities():
        real_city_count = str(get_real_city_count(i, current_data))
        try:
            expect_city_count = get_expect_city_count(i)
            rate = str('{:.2%}'.format(float(real_city_count) / float(expect_city_count)))
        except:
            expect_city_count = "0"
            rate = "0%"
        value = "('" + current_data + "','" + get_city_name(i) + "','" + expect_city_count + "','" \
                + real_city_count + "','" + "http://" + i + ".lianjia.com/ershoufang/" + "','" + rate
        insert_city(value)


def statistics_sub_location():
    for city in get_all_cities():
        f = open("./relation", "r")
        city_name = get_city_name(city)
        for info in f.readlines():
            if city_name in info.split("-")[0]:
                location = info.split("-")[1]
                sub_location = info.split("-")[2]
                url = info.split("-")[3]
                expect_location_count = get_expect_location_count(city, url)
                real_sub_location_count = get_real_sub_location_count(sub_location, current_data)
                if expect_location_count == "0":
                    rate = "0%"
                else:
                    rate = str('{:.2%}'.format(float(real_sub_location_count) / float(expect_location_count)))
                value = "('" + current_data + "','" + city_name + "','" + expect_location_count + "','" \
                        + str(
                    real_sub_location_count) + "','" + "http://" + city + ".lianjia.com" + url + "','" + location + "','" + sub_location + "','" + rate
                insert_sub_location(value)


def statistics_location():
    for city in get_all_cities():
        url = "https://" + city + ".lianjia.com/ershoufang/"
        count_in_page = 0
        city_name = get_city_name(city)
        while True:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page, "html.parser")
            error = soup.title.text
            if error == u"验证异常流量-链家网" or error == u"人机认证":
                count_in_page = count_in_page + 1
                time.sleep(600)
            else:
                break
        for link in soup.find_all("div", attrs={'data-role': "ershoufang"}):
            location_souce = link.find_all("div")[0]
            for location in location_souce.find_all("a"):
                sub_location = location.text
                expect_location_count = get_expect_location_count(city, location.get("href"))
                url_all = url + location.get("href")
                real_location_count = get_real_location_count(location.text)
                if expect_location_count == "0":
                    rate = "0%"
                else:
                    rate = str('{:.2%}'.format(float(real_location_count) / float(expect_location_count)))
                value = "('" + current_data + "','" + city_name + "','" + expect_location_count + "','" \
                        + str(
                    real_location_count) + "','" + url_all + "','" + sub_location + "','" + rate
                insert_location(value)


def statistics_all():
    statistics_city()
    statistics_location()
    statistics_sub_location()


if __name__ == '__main__':
    statistics_all()
