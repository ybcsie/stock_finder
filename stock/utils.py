from .c_api import stock
import datetime


def get_new_high(work_arr_cptr):
    opt_list = stock.work(work_arr_cptr, stock.WORK_TYPE_NEWHIGH)

    return opt_list


def get_attack(work_arr_cptr):
    t1 = datetime.datetime.now()
    opt_list = stock.work(work_arr_cptr, stock.WORK_TYPE_ATTACK)
    t2 = datetime.datetime.now()

    # print("attack: {} s".format((t2 - t1).total_seconds()))

    return opt_list


def get_idx_by_stock_id(stock_data_cptr_list, stock_id):
    for i, stock_data_cptr in enumerate(stock_data_cptr_list):
        if stock.get_stock_id(stock_data_cptr) == stock_id:
            return i

    return -1
