#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import pandas as pd
from datetime import datetime
import time
import io
from crawler_lottery import CrawlerLottery


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



if __name__ == '__main__':
    try:
        print("start-time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

        company = "weilian"
        company_list = {
            "aomen": "5",
            "libo": "2",
            "weilian": "293"
        }
        cid = company_list[company]

        create_csv(company)

        start = "20110101"
        end = "20180628"
        date_list = get_date_list(start, end)
        for d in date_list:
            CrawlerLottery(d, cid, company)

        print("end-time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    except Exception as e:
        print("exception-time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print(e)
        pass
