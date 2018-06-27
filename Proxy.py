# -*- coding: UTF-8 -*-

import threading
from requests.packages import urllib3
import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import time
import json
import io
import random

ips = []


def lottery_request(url, headers, proxies):
    response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
    return response


def crawler_data(company, dt, url, headers, proxies):
    html = lottery_request(url, headers, proxies)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='gb18030')
    tr_list = soup.find_all("tr")
    res_list = []
    for i in range(len(tr_list)):
        ##从第7行开始
        if i > 6 and i % 2 == 1:
            ##抓取水位
            data_fid = tr_list[i].attrs['data-fid']
            asian = get_asian(data_fid, headers, proxies)
            europe = get_europe(data_fid, headers, proxies)
            ###处理信息
            row = tr_list[i].contents

            riqi = dt
            saishi = row[3].text
            lunci = row[5].text
            bisaishijian = row[7].text
            zhudui = row[9].text
            kedui = row[13].text
            bifen = row[11].text
            gongsi = row[15].text

            if asian and europe is not None:
                yachupan_up = asian["yachupan_up"]
                yachupan_rang = asian["yachupan_rang"]
                yachupan_down = asian["yachupan_down"]
                yazhongpan_up = asian["yazhongpan_up"]
                yazhongpan_rang = asian["yazhongpan_rang"]
                yazhongpan_down = asian["yazhongpan_down"]

                ouchupan_win = europe["ouchupan_win"]
                ouchupan_draw = europe["ouchupan_draw"]
                ouchupan_loss = europe["ouchupan_loss"]
                ouzhongpan_win = europe["ouzhongpan_win"]
                ouzhongpan_draw = europe["ouzhongpan_draw"]
                ouzhongpan_loss = europe["ouzhongpan_loss"]

                strings = str(riqi) + ',' + str(saishi) + ',' + str(lunci) + ',' + str(bisaishijian) + ',' + str(
                    zhudui) + ',' + str(kedui) \
                          + ',' + str(bifen) + ',' + str(gongsi) + ',' + str(yachupan_up) + ',' + str(
                    yachupan_rang) + ',' + str(yachupan_down) \
                          + ',' + str(yazhongpan_up) + ',' + str(yazhongpan_rang) + ',' + str(
                    yazhongpan_down) + ',' + str(
                    ouchupan_win) \
                          + ',' + str(ouchupan_draw) + ',' + str(ouchupan_loss) + ',' + str(ouzhongpan_win) + ',' + str(
                    ouzhongpan_draw) + ',' + str(ouzhongpan_loss)

                res_list.append(u"%s" % strings)
    write_csv(company, res_list)


##获取亚盘水位
def get_asian(data_fid, headers, proxies):
    now = time.time()
    now_int = int(now)
    water_url = "http://odds.500.com/json/odds.php?_=" + str(
        now_int) + "&fid=" + data_fid + "&cid=3&type=asian&r=1"
    water = lottery_request(water_url, headers, proxies)
    if len(water.text) > 2:
        water_list = json.loads(water.text)
        water_first = water_list[len(water_list) - 1]
        yachupan_up = water_first[0]
        yachupan_rang = water_first[1]
        yachupan_down = water_first[2]
        water_end = water_list[0]
        yazhongpan_up = water_end[0]
        yazhongpan_rang = water_end[1]
        yazhongpan_down = water_end[2]
        dic = {
            "yachupan_up": yachupan_up,
            "yachupan_rang": yachupan_rang,
            "yachupan_down": yachupan_down,
            "yazhongpan_up": yazhongpan_up,
            "yazhongpan_rang": yazhongpan_rang,
            "yazhongpan_down": yazhongpan_down
        }
        return dic
    return None


def get_europe(data_fid, headers, proxies):
    now = time.time()
    now_int = int(now)
    water_url = "http://odds.500.com/json/odds.php?_=" + str(
        now_int) + "&fid=" + data_fid + "&cid=3&type=europe&r=1"
    water = lottery_request(water_url, headers, proxies)
    if len(water.text) > 2:
        water_list = json.loads(water.text)
        water_first = water_list[len(water_list) - 1]
        ouchupan_win = water_first[0]
        ouchupan_draw = water_first[1]
        ouchupan_loss = water_first[2]
        water_end = water_list[0]
        ouzhongpan_win = water_end[0]
        ouzhongpan_draw = water_end[1]
        ouzhongpan_loss = water_end[2]
        dic = {
            "ouchupan_win": ouchupan_win,
            "ouchupan_draw": ouchupan_draw,
            "ouchupan_loss": ouchupan_loss,
            "ouzhongpan_win": ouzhongpan_win,
            "ouzhongpan_draw": ouzhongpan_draw,
            "ouzhongpan_loss": ouzhongpan_loss
        }
        return dic
    return None


def create_csv(company):
    file = company + ".csv"
    headers = u"riqi,saishi,lunci,bisaishijian,zhudui,kedui,bifen,gongsi,yachupan_up,yachupan_rang,yachupan_down,yazhongpan_up,yazhongpan_rang," \
              u"yazhongpan_down,ouchupan_win,ouchupan_draw,ouchupan_loss,ouzhongpan_win,ouzhongpan_draw,ouzhongpan_loss"
    with io.open(file, mode="a", encoding='utf-8') as csvfile:
        csvfile.write(headers)
        csvfile.write(u'\n')


def write_csv(company, res_list):
    with io.open(company + ".csv", mode="a", encoding='utf-8') as csvfile:
        for line in res_list:
            csvfile.write(u"%s" % line)
            csvfile.write(u"\n")


def get_date_list(beginDate, endDate):
    # beginDate, endDate是形如‘20160601’的字符串或datetime格式
    date_list = [datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_list


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def handle(company, start, end, headers, proxies):
    date_list = get_date_list(start, end)
    for d in date_list:
        url = "http://odds.500.com/index_history_" + str(d) + ".shtml#!"
        crawler_data(company, d, url, headers, proxies)


# 爬数据的线程类
class CrawlThread(threading.Thread):
    def __init__(self, proxyip):
        super(CrawlThread, self).__init__()
        self.proxyip = proxyip

    def run(self):
        urllib3.disable_warnings()
        company = "Bet365"
        # create_csv(company)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        proxies = {"http": 'http://' + self.proxyip}
        handle(company, '20160202', '20180627', headers, proxies)


# 获取代理IP的线程类
class GetIpThread(threading.Thread):
    def __init__(self, fetchSecond):
        super(GetIpThread, self).__init__()
        self.fetchSecond = fetchSecond

    def run(self):
        global ips
        while True:
            # 获取IP列表
            res = requests.get(apiUrl).content.decode()
            # 按照\n分割获取到的IP
            ips = res.split('\n')
            # 利用每一个IP
            for proxyip in ips:
                # 开启一个线程
                CrawlThread(proxyip).start()
            # 休眠
            time.sleep(self.fetchSecond)


if __name__ == '__main__':
    # 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
    order = "74980f18b66cb3f3c92561b3a085ac63"
    # 获取IP的API接口
    apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
    # 要抓取的目标网站地址
    targetUrl = "http://ip.chinaz.com/getip.aspx"
    # 获取IP时间间隔，建议为5秒
    fetchSecond = 5
    # 开始自动获取IP
    GetIpThread(fetchSecond).start()
