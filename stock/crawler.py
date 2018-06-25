from . import msgopt, tools
import os
import datetime
import urllib.request
import json


logger = msgopt.Logger("crawler")


def get_day_trading_data(yyyymmdd):
    logger.logp("get_day_trading_data: {}".format(yyyymmdd))

    url = "http://www.twse.com.tw/exchangeReport/TWTB4U?response=json&date={}&selectType=All".format(yyyymmdd)

    tools.delay(3)  # delay

    max_try = 3
    while True:
        logger.logp("Trying connection...")
        from socket import timeout
        try:
            res = urllib.request.urlopen(url, timeout=5)
            logger.logp("OK")

        except timeout:
            logger.logp("Error: urllib -- timeout")
            tools.wait_retry(logger, 10)
            continue

        except :
            logger.logp("Error: urllib")
            tools.wait_retry(logger, 30)
            continue

        logger.logp("Trying json decode...")
        # check stat
        try:
            data = json.loads(res.read().decode())
            if data["stat"] != "OK":
                logger.logp("data error: stat = {}".format(data["stat"]))

                tools.wait_retry(logger, 5)
                if max_try == 0:
                    return None

                max_try -= 1
                continue

        except:
            logger.logp("Error: json when checking stat")
            tools.wait_retry(logger, 5)
            continue

        # check date
        try:
            if data["date"] != "{}".format(yyyymmdd):
                logger.logp("data error: date = {}".format(data["date"]))

                tools.wait_retry(logger, 5)
                if max_try == 0:
                    return None

                max_try -= 1
                continue

        except:
            logger.logp("Error: json when checking date")
            tools.wait_retry(logger, 5)
            continue

        # return
        return data["data"]
