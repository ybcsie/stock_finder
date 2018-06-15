#include "stock.h"
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

stock_data_arr *new_stock_data_arr_ptr(const int size)
{
	stock_data_arr *new_ptr = malloc(sizeof(stock_data_arr));
	new_ptr->ptr_arr = malloc(size * sizeof(stock_data *));
	new_ptr->size = size;
	new_ptr->cur_len_ptr = malloc(sizeof(int));

	*(new_ptr->cur_len_ptr) = 0;

	return new_ptr;
}

void del_stock_data_arr(stock_data_arr *stock_data_arr_ptr)
{
	for (int i = 0; i < *(stock_data_arr_ptr->cur_len_ptr) - 1; i++)
	{
		del_trade_day_info_arr(stock_data_arr_ptr->ptr_arr[i]->trade_day_info_arr_ptr);
		free(stock_data_arr_ptr->ptr_arr[i]);
	}

	free(stock_data_arr_ptr->ptr_arr);
	free(stock_data_arr_ptr->cur_len_ptr);
	free(stock_data_arr_ptr);
}

stock_data *new_stock_data_ptr(const int stock_id, const int ipo_date, const int trade_day_info_size)
{
	stock_data *new_ptr = malloc(sizeof(stock_data));
	new_ptr->stock_id = stock_id;
	new_ptr->ipo_date = ipo_date;
	new_ptr->trade_day_info_arr_ptr = new_trade_day_info_arr_ptr(trade_day_info_size);

	return new_ptr;
}

int get_stock_id(stock_data *stock_data_ptr) { return stock_data_ptr->stock_id; }

void add_stock_data(stock_data_arr *work_arr_ptr, stock_data *stock_data_ptr)
{
	*(work_arr_ptr->cur_len_ptr) += 1;
	assert(*(work_arr_ptr->cur_len_ptr) <= work_arr_ptr->size);

	work_arr_ptr->ptr_arr[*(work_arr_ptr->cur_len_ptr) - 1] = stock_data_ptr;
}

void add_trade_day_info(stock_data *stock_data_ptr, int date, float vol, float first, float highest, float lowest, float last, float delta)
{
	trade_day_info_arr *arr_ptr = stock_data_ptr->trade_day_info_arr_ptr;
	int arr_len = *(arr_ptr->cur_len_ptr);

	// check list empty
	if (arr_len > 0)
	{
		// not empty

		// check date
		// printf("%d %d %d\n", stock_data_ptr->stock_id, date, list_ptr->tail_ptr->date);
		// assert(date >= list_ptr->tail_ptr->date);
		if (arr_ptr->ptr_arr[arr_len - 1]->date == date)
		{
			update_trade_day_info_last_item(arr_ptr, date, vol, first, highest, lowest, last, delta);
			return;
		}
	}

	// add new node
	add_trade_day_info_new_item(arr_ptr, date, vol, first, highest, lowest, last, delta);
}

void set_days_range(int value) { days_range = value; }
void set_delta_percentage_min(float value) { delta_percentage_min = value; }
void set_price_limit(float value) { price_limit = value; }

static int (*work_funcs[])(trade_day_info **trade_day_info_ptr_arr, int trade_day_info_idx) = {is_new_high, is_attack};
const int WORK_TYPE_NEWHIGH = 0;
const int WORK_TYPE_ATTACK = 1;

PyObject *work(stock_data_arr *work_arr_ptr, const int work_type)
{
	PyObject *opt_PyList = PyList_New(0);

	trade_day_info_arr *trade_day_info_arr_ptr;
	for (int i = 0; i < *(work_arr_ptr->cur_len_ptr); i++)
	{
		trade_day_info_arr_ptr = work_arr_ptr->ptr_arr[i]->trade_day_info_arr_ptr;
		if (work_funcs[work_type](trade_day_info_arr_ptr->ptr_arr, *(trade_day_info_arr_ptr->cur_len_ptr) - 1))
			PyList_Append(opt_PyList, PyLong_FromLong(work_arr_ptr->ptr_arr[i]->stock_id));
	}

	return opt_PyList;
}

float calc_days_e(stock_data_arr *work_arr_ptr, const int days, const float mppt, const int buy_rule_no, const int RoI_rule_no)
{
	float er = 0; //E of win reward ratio

	trade_day_info_arr *trade_day_info_arr_ptr;
	int info_len;

	for (int i = 0; i < *(work_arr_ptr->cur_len_ptr); i++)
	{
		trade_day_info_arr_ptr = work_arr_ptr->ptr_arr[i]->trade_day_info_arr_ptr;
		info_len = *(trade_day_info_arr_ptr->cur_len_ptr);
		int start_idx = info_len - 1 - (days - 1);
		if (start_idx < 1)
			start_idx = 1;

		for (int trade_day_info_idx = start_idx; trade_day_info_idx < info_len; trade_day_info_idx++)
		{
			if (!is_buy_target(trade_day_info_arr_ptr->ptr_arr, trade_day_info_idx, mppt, buy_rule_no))
				continue; //not target

			er += get_RoI(trade_day_info_arr_ptr->ptr_arr, trade_day_info_idx, mppt, RoI_rule_no);
		}
	}

	// printf("total: %d\n", total);
	// printf("match: %d\n", match);
	// printf("possibility: %f%c\n", (float)match / total * 100, '%');
	printf("E of R: %f%c\n", er, '%');
	return er;
}

float calc_day_e(stock_data_arr *work_arr_ptr, const int date, const float mppt, const int buy_rule_no, const int RoI_rule_no)
{
	float er = 0; //E of win reward ratio

	trade_day_info_arr *trade_day_info_arr_ptr;
	int trade_day_info_idx;

	int no_target = 1;

	for (int i = 0; i < *(work_arr_ptr->cur_len_ptr); i++)
	{
		trade_day_info_arr_ptr = work_arr_ptr->ptr_arr[i]->trade_day_info_arr_ptr;

		trade_day_info_idx = find_idx_by_date(trade_day_info_arr_ptr, date);

		if (trade_day_info_idx == -1)
			continue;

		no_target = 0;

		if (!is_buy_target(trade_day_info_arr_ptr->ptr_arr, trade_day_info_idx, mppt, buy_rule_no))
			continue; //not target

		er += get_RoI(trade_day_info_arr_ptr->ptr_arr, trade_day_info_idx, mppt, RoI_rule_no);
	}

	if (no_target)
		er = -99999;
	else
		assert(er != -99999);

	printf("E of R: %f%c\n", er, '%');
	return er;
}

float calc_month_e(stock_data_arr *work_arr_ptr, const int yyyymm, const float mppt, const int buy_rule_no, const int RoI_rule_no)
{
	trade_day_info_arr *trade_day_info_arr_ptr;

	int no_target = 1;

	int start_idx;
	int end_idx;

	float er = 0; //E of win reward ratio

	for (int i = 0; i < *(work_arr_ptr->cur_len_ptr); i++)
	{
		trade_day_info_arr_ptr = work_arr_ptr->ptr_arr[i]->trade_day_info_arr_ptr;

		if (find_idx_range_by_yyyymm(trade_day_info_arr_ptr, yyyymm, &start_idx, &end_idx) != 0)
			continue;

		no_target = 0;

		for (int trade_day_info_idx = start_idx; trade_day_info_idx <= end_idx; trade_day_info_idx++)
		{
			if (!is_buy_target(trade_day_info_arr_ptr->ptr_arr, trade_day_info_idx, mppt, buy_rule_no))
				continue; //not target

			er += get_RoI(trade_day_info_arr_ptr->ptr_arr, trade_day_info_idx, mppt, RoI_rule_no);
		}
	}

	if (no_target)
		er = -99999;
	else
		assert(er != -99999);

	printf("E of R: %f%c\n", er, '%');
	return er;
}
