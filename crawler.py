#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import time
import json
import io
import random


def lottery_request(url, headers):
    response = requests.get(url, headers=headers, timeout=5)
    return response


def crawler_data(cid, dt, url, headers):
    html = lottery_request(url, headers)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding='gb18030')
    tr_list = soup.find_all("tr")
    res_list = []
    for i in range(len(tr_list)):
        ##从第7行开始
        if i > 6 and i % 2 == 1:
            ##抓取水位
            data_fid = tr_list[i].attrs['data-fid']
            asian = get_asian(cid, data_fid, headers)
            ##增加sleep时间
            sleep_time = random.randint(0, 5)
            time.sleep(sleep_time)
            europe = get_europe(cid, data_fid, headers)
            ###处理信息
            row = tr_list[i].contents

            riqi = dt
            saishi = row[3].text
            lunci = row[5].text
            bisaishijian = row[7].text
            zhudui = row[9].text
            kedui = row[13].text
            bifen = row[11].text

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
                          + ',' + str(bifen) + ',' + str(yachupan_up) + ',' + str(
                    yachupan_rang) + ',' + str(yachupan_down) \
                          + ',' + str(yazhongpan_up) + ',' + str(yazhongpan_rang) + ',' + str(
                    yazhongpan_down) + ',' + str(
                    ouchupan_win) \
                          + ',' + str(ouchupan_draw) + ',' + str(ouchupan_loss) + ',' + str(ouzhongpan_win) + ',' + str(
                    ouzhongpan_draw) + ',' + str(ouzhongpan_loss)

                res_list.append(u"%s" % strings)
    write_csv(company, res_list)
    sleep_time = random.randint(0, 120)
    time.sleep(sleep_time)


##获取亚盘水位
def get_asian(cid, data_fid, headers):
    now = time.time()
    now_int = int(now)
    water_url = "http://odds.500.com/json/odds.php?_=" + str(
        now_int) + "&fid=" + data_fid + "&cid=" + cid + "&type=asian&r=1"
    water = lottery_request(water_url, headers)
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


def get_europe(cid, data_fid, headers):
    now = time.time()
    now_int = int(now)
    water_url = "http://odds.500.com/json/odds.php?_=" + str(
        now_int) + "&fid=" + data_fid + "&cid=" + cid + "&type=asian&r=1"
    water = lottery_request(water_url, headers)
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
    headers = u"riqi,saishi,lunci,bisaishijian,zhudui,kedui,bifen,yachupan_up,yachupan_rang,yachupan_down,yazhongpan_up,yazhongpan_rang," \
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


def handle(start, end, cid, headers):
    date_list = get_date_list(start, end)
    for d in date_list:
        # proxies = get_random_ip(ip_list)
        # print("proxies:" + proxies["http"])
        url = "http://odds.500.com/index_history_" + str(d) + ".shtml#!"
        crawler_data(cid, d, url, headers)


if __name__ == '__main__':
    try:
        print("start-time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        url = 'http://www.xicidaili.com/nn/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        # ip_list = get_ip_list(url, headers=headers)
        ip_list = [
            "140.205.222.3:80",
            "117.127.0.205:8080",
        ]

        company = "aomen"
        company_list = {
            "aomen": "5",
            "libo": "2",
            "welian": "293"
        }

        create_csv(company)
        handle('20160101', '20180627', company_list[company], headers)

        print("end-time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    except Exception as e:
        print("exception-time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print(e)
        pass
