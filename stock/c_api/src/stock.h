#ifndef STOCK_H
#define STOCK_H

#include "stock_data.h"
#include <Python.h>

stock_data_arr *new_stock_data_arr_ptr(const int size);
void del_stock_data_arr(stock_data_arr *stock_data_arr_ptr);

stock_data *new_stock_data_ptr(const int stock_id, const int ipo_date, const int trade_day_info_size);

int get_stock_id(stock_data *stock_data_ptr);

void add_stock_data(stock_data_arr *work_arr_ptr, stock_data *stock_data_ptr);

void add_trade_day_info(stock_data *stock_data_ptr, const int date, const float vol, const float first, const float highest, const float lowest, const float last, const float delta);

void set_days_range(int value);
void set_delta_percentage_min(float value);

extern const int WORK_TYPE_NEWHIGH;
extern const int WORK_TYPE_ATTACK;
PyObject *work(stock_data_arr *work_arr_ptr, const int work_type);
void calc_p(stock_data_arr *work_arr_ptr, const int days, const float percentage);

#endif
