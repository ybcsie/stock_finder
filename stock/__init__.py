from .c_api import stock
from . import reader, livedata, tools, updater
from .utils import get_new_high, get_attack
from .msgopt import Logger


def init_work_arr(stock_data_cptr_list):
    stock_arr_cptr = stock.new_stock_data_arr_ptr(len(stock_data_cptr_list))
    for stock_data_cptr in stock_data_cptr_list:
        stock.add_stock_data(stock_arr_cptr, stock_data_cptr)

    return stock_arr_cptr

