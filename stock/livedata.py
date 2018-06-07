from . import tools, msgopt, utils, reader
from .c_api import stock
import datetime
import time
import json
import urllib.request
import http.cookiejar


logger = msgopt.Logger("livedata")


def get_livedata(stock_data_cptr_list):
    now = datetime.datetime.now()
    if (7 * 60 + 30) < (now.hour * 60 + now.minute) < (8 * 60 + 30):
        return

    logger.logp("get_livedata : start")
    size = len(stock_data_cptr_list)
    cptr_list_list = []
    if size > 100:
        for i in range(0, size, 100):
            cptr_list_list.append(stock_data_cptr_list[i:i + 100])

    delay = 4
    connection_end_datetime = None
    for i, cur_cptr_list in enumerate(cptr_list_list):
        logger.logp("get live data {} / {}".format(i + 1, len(cptr_list_list)))
        max_try = 3
        while max_try > 0:
            if connection_end_datetime is not None:
                tools.delay_from_datetime(connection_end_datetime, delay)
            else:
                tools.delay(delay)

            try:
                url = "http://163.29.17.179/stock/fibest.jsp"
                cookie = http.cookiejar.CookieJar()
                handler = urllib.request.HTTPCookieProcessor(cookie)
                opener = urllib.request.build_opener(handler)
                opener.open(url)

                stock_arg = ""
                for stock_data_cptr in cur_cptr_list:
                    stock_arg += "tse_{}.tw|".format(stock.get_stock_id(stock_data_cptr))

                arg = "getStockInfo.jsp?ex_ch={}&json=1&delay=0&_={}".format(stock_arg, int(time.time() * 1000))
                url = "http://163.29.17.179/stock/api/" + arg
                # input(url)
                request = urllib.request.Request(url)
                res = opener.open(request, timeout=5)
                connection_end_datetime = datetime.datetime.now()

            except:
                connection_end_datetime = datetime.datetime.now()
                logger.logp("Error: connection")
                max_try -= 1
                continue

            # StockData.display("Trying json decode...")
            try:
                live_data = json.loads(res.read().decode())
                # print(live_data["rtmessage"])
                if live_data["rtmessage"] != "OK":
                    logger.logp("Error: data")
                    max_try -= 1
                    continue

            except:
                logger.logp("Error: json")
                max_try -= 1
                continue

            load_livedata(live_data["msgArray"], cur_cptr_list)
            break

    # StockData.live_last_update_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    logger.logp("get_livedata : Done")


def load_livedata(livedata_list, stock_data_cptr_list):
    for livedata in livedata_list:
        livedata_stock_id = int(livedata["c"])
        idx = utils.get_idx_by_stock_id(stock_data_cptr_list, livedata_stock_id)
        if idx < 0:
            logger.logp("stock id {} not in list".format(livedata_stock_id))
            continue

        reader.read_livedata(livedata, stock_data_cptr_list[idx])


