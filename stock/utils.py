from .c_api import stock
import datetime


def get_new_high(work_arr_cptr, days_range, delta_percentage_min):
    stock.set_days_range(days_range)
    stock.set_days_range(delta_percentage_min)
    opt_list = stock.work(work_arr_cptr, stock.WORK_TYPE_NEWHIGH)

    return opt_list


def get_attack(work_arr_cptr, days_range, delta_percentage_min):
    stock.set_days_range(days_range)
    stock.set_days_range(delta_percentage_min)
    opt_list = stock.work(work_arr_cptr, stock.WORK_TYPE_ATTACK)

    return opt_list


def cal_p(work_arr_cptr, days_range, delta_percentage_min, days, percentage):
    stock.set_days_range(days_range)
    stock.set_days_range(delta_percentage_min)
    stock.calc_p(work_arr_cptr, days, percentage)


def get_idx_by_stock_id(stock_data_cptr_list, stock_id):
    for i, stock_data_cptr in enumerate(stock_data_cptr_list):
        if stock.get_stock_id(stock_data_cptr) == stock_id:
            return i

    return -1
