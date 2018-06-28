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
from retrying import retry
import threading


def retry_if_result_none(result):
    return result is None


def get_date_list(beginDate, endDate):
    date_list = [datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_list


def create_csv(company):
    file = company + ".csv"
    headers = u"riqi,saishi,lunci,bisaishijian,zhudui,kedui,bifen,yachupan_up,yachupan_rang,yachupan_down,yazhongpan_up,yazhongpan_rang," \
              u"yazhongpan_down,ouchupan_win,ouchupan_draw,ouchupan_loss,ouzhongpan_win,ouzhongpan_draw,ouzhongpan_loss"
    with io.open(file, mode="a", encoding='utf-8') as csvfile:
        csvfile.write(headers)
        csvfile.write(u'\n')


class CrawlerLottery(threading.Thread):
    proxy = ""
    weilian_cid = "293"

    def __init__(self, date, cid, headers):
        super(CrawlerLottery, self).__init__()
        self.handle(date, cid, headers)

    def handle(self, date, cid, headers):
        self.proxy = ""
        url = "http://odds.500.com/index_history_" + str(date) + ".shtml#!"
        self.crawler_data(cid, date, url, headers, self.proxy)

    def lottery_request(self, url, headers, proxy):
        try:
            print(url)
            response = requests.get(url, headers=headers, timeout=5, proxies=proxy)
            if response is not None:
                return response
            return None
        except Exception:
            pass

    def lottery_sleep(a, b):
        sleep_time = random.randint(a, b)
        time.sleep(sleep_time)

    @retry(retry_on_result=retry_if_result_none)
    def crawler_data(self, cid, dt, url, headers, proxy):
        try:
            print(url)
            html = self.lottery_request(url, headers, proxy)
            if html is not None:
                soup = BeautifulSoup(html.content, 'html.parser', from_encoding='gb18030')
                tr_list = soup.find_all("tr")
                res_list = []
                for i in range(len(tr_list)):
                    ##from line 7
                    if i > 6 and i % 2 == 1:
                        row = tr_list[i].contents
                        riqi = dt
                        saishi = row[3].text
                        lunci = row[5].text
                        bisaishijian = row[7].text
                        zhudui = row[9].text
                        kedui = row[13].text
                        bifen = row[11].text

                        data_fid = tr_list[i].attrs['data-fid']

                        yachupan_up = " "
                        yachupan_rang = " "
                        yachupan_down = " "
                        yazhongpan_up = " "
                        yazhongpan_rang = " "
                        yazhongpan_down = " "

                        if cid != self.weilian_cid:
                            asian = self.get_asian(cid, data_fid, headers, proxy)
                            if asian is not None:
                                yachupan_up = asian["yachupan_up"]
                                yachupan_rang = asian["yachupan_rang"]
                                yachupan_down = asian["yachupan_down"]
                                yazhongpan_up = asian["yazhongpan_up"]
                                yazhongpan_rang = asian["yazhongpan_rang"]
                                yazhongpan_down = asian["yazhongpan_down"]

                        europe = self.get_europe(cid, data_fid, headers, proxy)
                        if europe is not None:
                            ouchupan_win = europe["ouchupan_win"]
                            ouchupan_draw = europe["ouchupan_draw"]
                            ouchupan_loss = europe["ouchupan_loss"]
                            ouzhongpan_win = europe["ouzhongpan_win"]
                            ouzhongpan_draw = europe["ouzhongpan_draw"]
                            ouzhongpan_loss = europe["ouzhongpan_loss"]

                            strings = str(riqi) + ',' + str(saishi) + ',' + str(lunci) + ',' + str(
                                bisaishijian) + ',' + str(
                                zhudui) + ',' + str(kedui) \
                                      + ',' + str(bifen) + ',' + str(yachupan_up) + ',' + str(
                                yachupan_rang) + ',' + str(yachupan_down) \
                                      + ',' + str(yazhongpan_up) + ',' + str(yazhongpan_rang) + ',' + str(
                                yazhongpan_down) + ',' + str(
                                ouchupan_win) \
                                      + ',' + str(ouchupan_draw) + ',' + str(ouchupan_loss) + ',' + str(
                                ouzhongpan_win) + ',' + str(
                                ouzhongpan_draw) + ',' + str(ouzhongpan_loss)

                            res_list.append(u"%s" % strings)
                self.write_csv(company, res_list)
            return True
        except Exception as e:
            print("crawler_data is error:" + str(e))
            # self.proxy = self.get_proxy()
            return None

    def get_asian(self, cid, data_fid, headers, proxy):
        now = time.time()
        now_int = int(now)
        water_url = "http://odds.500.com/json/odds.php?_=" + str(
            now_int) + "&fid=" + data_fid + "&cid=" + cid + "&type=asian&r=1"
        water = self.lottery_request(water_url, headers, proxy)
        if water is not None:
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

    def get_europe(self, cid, data_fid, headers, proxy):
        now = time.time()
        now_int = int(now)
        water_url = "http://odds.500.com/json/odds.php?_=" + str(
            now_int) + "&fid=" + data_fid + "&cid=" + cid + "&type=europe&r=1"
        water = self.lottery_request(water_url, headers, proxy)
        if water is not None:
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

    def write_csv(self, company, res_list):
        with io.open(company + ".csv", mode="a", encoding='utf-8') as csvfile:
            for line in res_list:
                csvfile.write(u"%s" % line)
                csvfile.write(u"\n")

    def get_ip_list(self, url, headers):
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].text + ':' + tds[2].text)
        return ip_list

    def get_random_ip(self, ip_list):
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        return proxies

    def get_proxy(self):
        order = "74980f18b66cb3f3c92561b3a085ac63"
        apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
        res = requests.get(apiUrl).content.decode()
        ips = res.split('\n')
        print("check-proxy:" + ips[0])
        proxy = {"http": ips[0]}
        check = self.check_proxy(proxy)
        if check is True:
            print("proxy-ok:" + ips[0])
            return proxy

    def check_proxy(self, proxy):
        url = "http://odds.500.com/index_history_2016-01-01.shtml#!"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        try:
            html = self.lottery_request(url, headers, proxy)
            if html is not None:
                return True
            return False
        except:
            return False


if __name__ == '__main__':
    try:
        print("start-time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }

        company = "weilian"
        company_list = {
            "aomen": "5",
            "libo": "2",
            "weilian": "293"
        }
        cid = company_list[company]

        start = "20110101"
        end = "20180628"
        date_list = get_date_list(start, end)
        for d in date_list:
            CrawlerLottery(d, cid, headers)
        print("end-time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    except Exception as e:
        print("exception-time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print(e)
        pass
