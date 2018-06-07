#include "stock_data.h"
#include "tools.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

trade_day_info_arr *new_trade_day_info_arr_ptr(const int size)
{
	trade_day_info_arr *new_ptr = malloc(sizeof(trade_day_info_arr));
	new_ptr->ptr_arr = malloc(sizeof(trade_day_info *) * size);
	new_ptr->cur_len_ptr = malloc(sizeof(int));
	new_ptr->size = size;

	*(new_ptr->cur_len_ptr) = 0;

	return new_ptr;
}

void del_trade_day_info_arr(trade_day_info_arr *trade_day_info_arr_ptr)
{
	for (int i = 0; i < *(trade_day_info_arr_ptr->cur_len_ptr) - 1; i++)
		free(trade_day_info_arr_ptr->ptr_arr[i]);

	free(trade_day_info_arr_ptr->ptr_arr);
	free(trade_day_info_arr_ptr->cur_len_ptr);
	free(trade_day_info_arr_ptr);
}

void add_trade_day_info_new_item(trade_day_info_arr *trade_day_info_arr_ptr, int date, float vol, float first, float highest, float lowest, float last, float delta)
{
	assert(*(trade_day_info_arr_ptr->cur_len_ptr) < trade_day_info_arr_ptr->size);
	*(trade_day_info_arr_ptr->cur_len_ptr) += 1;

	trade_day_info *new_trade_day_info_ptr = malloc(sizeof(trade_day_info));

	new_trade_day_info_ptr->date = date;
	new_trade_day_info_ptr->vol = vol;
	new_trade_day_info_ptr->first = first;
	new_trade_day_info_ptr->highest = highest;
	new_trade_day_info_ptr->lowest = lowest;
	new_trade_day_info_ptr->last = last;
	new_trade_day_info_ptr->delta = delta;

	trade_day_info_arr_ptr->ptr_arr[*(trade_day_info_arr_ptr->cur_len_ptr) - 1] = new_trade_day_info_ptr;
}

void update_trade_day_info_last_item(trade_day_info_arr *trade_day_info_arr_ptr, int date, float vol, float first, float highest, float lowest, float last, float delta)
{
	trade_day_info *last_item_ptr = trade_day_info_arr_ptr->ptr_arr[*(trade_day_info_arr_ptr->cur_len_ptr) - 1];

	// check empty
	assert(*(trade_day_info_arr_ptr->cur_len_ptr) > 0);

	// check date
	assert(date == last_item_ptr->date);

	// replace last
	last_item_ptr->vol = vol;
	last_item_ptr->first = first;
	last_item_ptr->highest = highest;
	last_item_ptr->lowest = lowest;
	last_item_ptr->last = last;
	last_item_ptr->delta = delta;
}

int find_highest_idx(trade_day_info **trade_day_info_ptr_arr, int trade_day_info_idx, int earliest_date)
{
	int highest_idx = trade_day_info_idx;

	for (int i = trade_day_info_idx - 1; i >= 0; i--)
	{
		// is date in bound?
		if (trade_day_info_ptr_arr[i]->date >= earliest_date)
		{
			if (trade_day_info_ptr_arr[i]->highest > trade_day_info_ptr_arr[highest_idx]->highest)
				highest_idx = i;
		}
		else
			break;
	}

	return highest_idx;
}

float get_delta_percentage(trade_day_info **trade_day_info_ptr_arr, int trade_day_info_idx)
{
	if (trade_day_info_idx == 0)
		return 0;

	return trade_day_info_ptr_arr[trade_day_info_idx]->delta / trade_day_info_ptr_arr[trade_day_info_idx - 1]->last * 100;
}

int is_red_k(trade_day_info *trade_day_info_ptr)
{
	if (trade_day_info_ptr->last > trade_day_info_ptr->first)
		return 1; //true

	return 0; //false
}

int is_new_high(trade_day_info **trade_day_info_ptr_arr, int trade_day_info_idx, int days_range, int delta_percentage_min)
{
	if (trade_day_info_idx == 0)
		return 0; //false

	if (!is_red_k(trade_day_info_ptr_arr[trade_day_info_idx]))
		return 0; //false

	if (get_delta_percentage(trade_day_info_ptr_arr, trade_day_info_idx) < delta_percentage_min)
		return 0; //false

	int earliest_date = get_date_by_delta(trade_day_info_ptr_arr[trade_day_info_idx]->date, days_range);

	int highest_idx = find_highest_idx(trade_day_info_ptr_arr, trade_day_info_idx, earliest_date);

	assert(highest_idx >= 0);

	if (highest_idx == trade_day_info_idx)
		return 1; //true

	return 0; //false
}

int is_jump(trade_day_info **trade_day_info_ptr_arr, int trade_day_info_idx)
{
	// check is first?
	if (trade_day_info_idx == 0)
		return 0; //false

	if (trade_day_info_ptr_arr[trade_day_info_idx]->first > trade_day_info_ptr_arr[trade_day_info_idx - 1]->highest)
		return 1; //true

	return 0; //false
}

int has_gap(trade_day_info **trade_day_info_ptr_arr, int trade_day_info_idx)
{
	// check is first?
	if (trade_day_info_idx == 0)
		return 0; //false

	if (trade_day_info_ptr_arr[trade_day_info_idx]->lowest > trade_day_info_ptr_arr[trade_day_info_idx - 1]->highest)
		return 1; //true

	return 0; //false
}

int is_attack(trade_day_info **trade_day_info_ptr_arr, int trade_day_info_idx, int days_range, int delta_percentage_min)
{
	// check is first?
	if (trade_day_info_idx == 0)
		return 0; //false

	if (!is_new_high(trade_day_info_ptr_arr, trade_day_info_idx - 1, days_range, delta_percentage_min))
		return 0; //false

	if (has_gap(trade_day_info_ptr_arr, trade_day_info_idx))
		return 1; //true

	return 0; //false
}
