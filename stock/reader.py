from . import tools, msgopt
from .c_api import stock
import os
import json
import datetime


logger = msgopt.Logger("reader")


def read_stock_data_cptr_list(sid_path, trade_day_size):
    if not os.path.exists(sid_path):
        raise RuntimeError("{} not exist".format(sid_path))

    sid_reader = open(sid_path, 'r', encoding="UTF-8")
    stock_data_cptr_list = sid_reader.read().split(';')
    sid_reader.close()

    for i in range(len(stock_data_cptr_list)):
        stock_info = stock_data_cptr_list[i].split(',')
        if len(stock_info) == 2:
            stock_data_cptr_list[i] = stock.new_stock_data_ptr(int(stock_info[0]),
                                                               tools.date2int(stock_info[1]),
                                                               trade_day_size)
        else:
            print("Error: stock list -- {}".format(stock_data_cptr_list[i]))

    return stock_data_cptr_list


def read_trade_day_list(smd_path, stock_data_cptr, months):
    if not os.path.exists(smd_path):
        raise RuntimeError("{} not exist".format(smd_path))

    # read
    smd_file = open(smd_path, 'r', encoding="UTF-8")
    content_dict = json.loads(smd_file.read())

    now = datetime.datetime.now()
    cur_month = now.month
    cur_year = now.year

    key_list = []

    for i in range(months):
        if cur_month == 0:
            cur_month = 12
            cur_year -= 1

        key = "{}{:02d}".format(cur_year, cur_month)
        trade_day_list = content_dict.get(key)
        if trade_day_list is not None:
            if len(trade_day_list) > 0:
                key_list.append(key)

        cur_month -= 1

    for key in reversed(key_list):
        for trade_day in content_dict[key]:
            if not (trade_day[3] == trade_day[4] == trade_day[5] == trade_day[6] == "--"):
                stock.add_trade_day_info(stock_data_cptr, tools.tw_date2int(trade_day[0]),
                                         tools.float_parser(trade_day[1]), tools.float_parser(trade_day[3]),
                                         tools.float_parser(trade_day[4]), tools.float_parser(trade_day[5]),
                                         tools.float_parser(trade_day[6]), tools.float_parser(trade_day[7]))

    smd_file.close()


def read_trade_data_in_list(trade_data_dir, stock_data_cptr_list, months):
    for stock_data_cptr in stock_data_cptr_list:
        stock_id = stock.get_stock_id(stock_data_cptr)
        print("read trade data {}".format(stock_id))
        read_trade_day_list("{}/{}.smd".format(trade_data_dir, stock_id), stock_data_cptr, months)


def read_livedata(livedata, stock_data_cptr):
    try:
        date = int(livedata["d"])
    except:
        logger.logp("Error: livedata date -- {} {}".format(stock.get_stock_id(stock_data_cptr), livedata))
        return

    try:
        vol = tools.float_parser(livedata["v"])
    except KeyError:
        vol = 0.0

    try:
        first = tools.float_parser(livedata["o"])
    except KeyError:
        try:
            first = tools.float_parser(livedata["pz"])
        except KeyError:
            first = 0.0

    try:
        highest = tools.float_parser(livedata["h"])
    except KeyError:
        try:
            highest = tools.float_parser(livedata["pz"])
        except KeyError:
            highest = 0.0

    try:
        lowest = tools.float_parser(livedata["l"])
    except KeyError:
        try:
            lowest = tools.float_parser(livedata["pz"])
        except KeyError:
            lowest = 0.0

    try:
        last = tools.float_parser(livedata["z"])
    except KeyError:
        try:
            last = tools.float_parser(livedata["pz"])
        except KeyError:
            last = 0.0

    try:
        delta = last - tools.float_parser(livedata["y"])
    except KeyError:
        delta = 0.0

    stock.add_trade_day_info(stock_data_cptr, date, vol, first, highest, lowest, last, delta)
