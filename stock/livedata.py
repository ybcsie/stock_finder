from . import tools, msgopt, utils, reader
from .c_api import stock
import json
import urllib.request


logger = msgopt.Logger("livedata")


def get_livedata(stock_data_cptr_list):
    logger.logp("get live data")
    max_try = 3
    while max_try > 0:
        try:
            url = "http://140.116.39.233/stockserver"
            res = urllib.request.urlopen(url, timeout=5)
            data = json.loads(res.read().decode())

        except:
            logger.logp("Error: connection")
            max_try -= 1
            tools.delay(1)
            continue

        try:
            stat = data["stat"]
            livedata_dict = data["livedata"]
            if stat != "OK":
                if stat == "LOADING":
                    return
                logger.logp("Error: stat : {}".format(stat))

        except:
            logger.logp("Error: json")
            max_try -= 1
            tools.delay(1)
            continue

        for key, value in livedata_dict.items():
            stock_id = int(key)
            idx = utils.get_idx_by_stock_id(stock_data_cptr_list, stock_id)
            if idx < 0:
                logger.logp("stock id {} not in list".format(stock_id))
                continue

            stock.add_trade_day_info(stock_data_cptr_list[idx], value[0], value[1], value[2], value[3], value[4],
                                     value[5], value[6])
        return


def load_livedata(livedata_list, stock_data_cptr_list):
    for livedata in livedata_list:
        livedata_stock_id = int(livedata["c"])
        idx = utils.get_idx_by_stock_id(stock_data_cptr_list, livedata_stock_id)
        if idx < 0:
            logger.logp("stock id {} not in list".format(livedata_stock_id))
            continue

        reader.read_livedata(livedata, stock_data_cptr_list[idx])


