#ifndef STOCK_H
#define STOCK_H

#include "stock_data.h"
#include <Python.h>

extern const int WORK_TYPE_NEWHIGH;
extern const int WORK_TYPE_ATTACK;

stock_data_arr *new_stock_data_arr_ptr(const int size);
stock_data *new_stock_data_ptr(const int stock_id, const int ipo_date);

int get_stock_id(stock_data *stock_data_ptr);

void add_stock_data(stock_data_arr *work_arr_ptr, stock_data *stock_data_ptr);

void add_trade_day_info(stock_data *stock_data_ptr, const int date, const float vol, const float first, const float highest, const float lowest, const float last, const float delta);

PyObject *work(stock_data_arr *work_arr_ptr, const int work_type);

#endif
