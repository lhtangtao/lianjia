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
import os.path
import re
import sys
import urllib2
import time
import thread
import threading
import datetime
from bs4 import BeautifulSoup
from my_sqldb import get_row, create_table, insert_info
from cities import get_city_name, get_sub_location
from file_action import read_sub_location, write_sub_location, delete_file_line, delete_file, get_all_cities, \
    spilt_file, get_all_cities_to_collect

reload(sys)
sys.setdefaultencoding('utf-8')
current_data = time.strftime('%Y-%m', time.localtime(time.time()))
time.clock()


def continue_action():
    while True:
        source = raw_input(u"请输入任意键后按回车继续")
        if source != "111111":
            result = True
            break
    print u"已解除封印，可继续执行"
    return result


def get_house(city="HZ", sub_location="/ershoufang/jinshahu/", file_add="   "):
    current_page = 1  # 当前在第几页
    total_page = 100  # 在这个区里一共有多少页房产信息
    while current_page <= total_page:  # 遍历这个区域的所有房子的信息
        url = "http://" + city + ".lianjia.com" + sub_location + 'pg' + str(current_page) + '/'
        count_in_page = 0
        while True:
            page = urllib2.urlopen(url)
            print file_add + "     " + url + u"开始采集"
            soup = BeautifulSoup(page, "html.parser")
            error = soup.title.text
            if error == u"验证异常流量-链家网" or error == u"人机认证":
                print file_add + u"  计数为" + str(count_in_page) + u' 在这个页面需要等待10分钟 ' + url + u" 现在时间是 " + time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime())
                count_in_page = count_in_page + 1
                time.sleep(600)
                # continue_action()
            else:
                break

        if current_page == 1:  # 第一页和最后一页 location_chinese的名字都是一样的
            for link in soup.find_all('div', 'resultDes clear'):
                context = link.get_text()
                # print context #示例是   共找到 3435 套滨江二手房with(document)write('<a
                # href="/ershoufang/"><span></span>清空条件</a>');保存搜索
                total_house = re.findall(r"\d+\.?\d*", context)[0]  # 总共有多少套房子
                print sub_location + u'一共有' + total_house + u'套房子'
                total_page = int(total_house) / 30 + 1  # 求出一共有多少页
                if total_page > 100:
                    total_page = 100
            file_address = "./relation"
            test = open(file_address, "r+")
            for line in test:
                if sub_location in line:
                    city_name = line.split("-")[0]
                    location_chinese = line.split("-")[1]
                    sub_location_chinese = line.split("-")[2]

        else:
            pass
        list_village = []
        for positionInfo in soup.find_all('div', 'positionInfo'):
            village = positionInfo.get_text()
            village_new = ""
            if len(village.split("-")) > 2:
                village = village.replace(" ", "")
                for i in range(len(village.split("-")) - 1):
                    village_new = village_new + village.split("-")[i]
                village = village_new

            else:
                # sub_location = village.split('-')[1].strip()
                village = village.split('-')[0].strip()
            list_village.append(village)
            # list_sub_location.append(sub_location)

        list_house_type = []
        list_square = []
        list_orientation = []
        list_decorate = []
        for link in soup.find_all('div', 'houseInfo'):  # 房子的相关信息，排除出各种别墅
            context = link.get_text()
            house_type = context.split('|')[0]
            square = context.split('|')[1][:-3]  # 把平米两个字去掉
            orientation = context.split('|')[3]
            if u'别墅' in house_type:
                house_type = context.split('|')[2]
                square = context.split('|')[3][:-3]  # 把平米两个字去掉
                orientation = context.split('|')[4]
            if len(context.split("|")) >= 5:
                decorate = context.split('|')[4]
            else:
                decorate = " "
            list_decorate.append(decorate)
            list_house_type.append(house_type)
            list_square.append(square)
            list_orientation.append(orientation)
        list_money = []
        i = 0
        list_temp = []
        for price in soup.find_all('div', 'totalPrice'):  # 总价的信息
            if u"暂无价格" in price.get_text():
                money = " "
                list_temp.append(i)
            else:
                money = price.get_text()
                money = money[:-1]  # 把最后的一个万字去掉
            i = i + 1
            list_money.append(money)
        list_per_square = []

        for price in soup.find_all('div', 'unitPrice'):  # 单价的信息
            per_square = price.get_text()
            per_square = per_square.replace(",", "").replace("元/平", '')
            list_per_square.append(per_square)
        for j in range(len(list_temp)):
            list_per_square.insert(list_temp[j], " ")

        list_url_text = []
        temp = 0
        for price in soup.find_all("a",
                                   attrs={'class': "noresultRecommend img LOGCLICKDATA"}):  # 获取链接
            url_text = price.get('href')
            list_url_text.append(url_text)
        for i in range(len(list_money)):
            try:
                message = insert_info(
                    '"' + current_data + '","' + city_name + '","' + location_chinese + '","' + sub_location_chinese + '","' +
                    list_village[
                        i] + '","' + list_house_type[
                        i] + '","' + list_square[i] + '","' + list_orientation[i] + '","' + list_decorate[i] + '","' +
                    list_money[
                        i] + '","' + list_per_square[i] + '","' + list_url_text[i] + '","' + str(
                        current_page) + '","' + url + '"')

            except:
                pass
        current_page += 1
    delete_file_line(city, sub_location)


def collect_by_file(city_to_collect="SX", file_add="./city_file/" + "SX0"):
    """
    根据传入的文件地址进行获取数据
    :param city_to_collect:
    :param file_add:
    :return:
    """
    localtion_list = read_sub_location(file_add)
    for sub_localtion in localtion_list:
        now_time_start = datetime.datetime.now()  # 现在
        print sub_localtion + u"开始时间" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        get_house(city_to_collect, sub_localtion, file_add)
        now_time_end = datetime.datetime.now()  # 现在
        print sub_localtion + u'已采集完毕 ' + str((now_time_end - now_time_start))
        print sub_localtion + u"结束时间" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print u"强制等待10秒"
        time.sleep(10 * 1)
    delete_file(file_add)


def gather(city_to_collect="HZ"):
    now_time_start_all = datetime.datetime.now()  # 现在
    exist_file_address = []
    if os.path.exists("./city_file/" + city_to_collect):
        collect_by_file(city_to_collect, "./city_file/" + city_to_collect)
    else:
        for i in range(10):
            file_address = "./city_file/" + city_to_collect + str(i)
            if os.path.exists(file_address):
                if os.path.getsize(file_address) == 0:
                    delete_file(file_address)
                else:
                    exist_file_address.append(file_address)
        if len(exist_file_address) == 0:
            print u'该城市的数据已经采集完毕'
        else:
            for x in range(len(exist_file_address)):
                threading.Thread(target=collect_by_file, args=(city_to_collect, exist_file_address[x])).start()
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    now_time_end = datetime.datetime.now()  # 现在
    print (now_time_end - now_time_start_all)  # 计算时间差


def get_all_sub_location():
    """
    step1
    区域信息更新了才要调用这个 这个函数一般一个月或者半年执行一次就够了
    :return:
    """
    start_time = time.time()
    location_list = get_all_cities()
    print location_list
    for i in location_list:
        write_sub_location(i)
    end_time = time.time()
    print u'Running time: %s Seconds' % (end_time - start_time)


if __name__ == '__main__':
    start = len(get_all_cities_to_collect())
    count = 0
    while True:
        end = len(get_all_cities_to_collect())
        if start - end == count:
            gather(get_all_cities_to_collect()[0])
            count = count + 1
        if count == start:
            break
        else:
            time.sleep(300)
