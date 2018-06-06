#include "stock_data.h"
#include "tools.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

trade_day_info_dllist *new_trade_day_info_dllist_ptr()
{
	trade_day_info_dllist *new_ptr = malloc(sizeof(trade_day_info_dllist));
	new_ptr->head_ptr = NULL;
	new_ptr->tail_ptr = NULL;
	new_ptr->list_len = 0;

	return new_ptr;
}

void add_trade_day_info_new_node(stock_data *stock_data_ptr, int date, float vol, float first, float highest, float lowest, float last, float delta)
{
	trade_day_info_dllist *list_ptr = stock_data_ptr->trade_day_info_list_ptr;

	trade_day_info *new_trade_day_info_ptr = malloc(sizeof(trade_day_info));

	new_trade_day_info_ptr->prev_ptr = list_ptr->tail_ptr;
	new_trade_day_info_ptr->next_ptr = NULL;

	new_trade_day_info_ptr->date = date;
	new_trade_day_info_ptr->vol = vol;
	new_trade_day_info_ptr->first = first;
	new_trade_day_info_ptr->highest = highest;
	new_trade_day_info_ptr->lowest = lowest;
	new_trade_day_info_ptr->last = last;
	new_trade_day_info_ptr->delta = delta;

	// modify list info
	if (list_ptr->list_len > 0)
	{
		assert(list_ptr->head_ptr != NULL && list_ptr->tail_ptr != NULL);
		list_ptr->tail_ptr->next_ptr = new_trade_day_info_ptr;
	}
	else
	{
		assert(list_ptr->list_len == 0);
		list_ptr->head_ptr = new_trade_day_info_ptr;
	}

	list_ptr->tail_ptr = new_trade_day_info_ptr;
	list_ptr->list_len += 1;
}

void update_trade_day_info_last_node(stock_data *stock_data_ptr, int date, float vol, float first, float highest, float lowest, float last, float delta)
{
	trade_day_info_dllist *list_ptr = stock_data_ptr->trade_day_info_list_ptr;

	// check empty
	assert(list_ptr->list_len > 0);
	assert(list_ptr->head_ptr != NULL && list_ptr->tail_ptr != NULL);

	// check date
	assert(date == list_ptr->tail_ptr->date);

	// replace last
	list_ptr->tail_ptr->date = date;
	list_ptr->tail_ptr->vol = vol;
	list_ptr->tail_ptr->first = first;
	list_ptr->tail_ptr->highest = highest;
	list_ptr->tail_ptr->lowest = lowest;
	list_ptr->tail_ptr->last = last;
	list_ptr->tail_ptr->delta = delta;
}

trade_day_info *find_highest_ptr(trade_day_info *trade_day_info_ptr, int earliest_date)
{
	trade_day_info *highest_ptr = trade_day_info_ptr;
	trade_day_info *cur_ptr = trade_day_info_ptr->prev_ptr;
	while (cur_ptr != NULL)
	{
		// is date in bound?
		if (cur_ptr->date >= earliest_date)
		{
			if (cur_ptr->highest > highest_ptr->highest)
				highest_ptr = cur_ptr;
		}
		else
			break;

		cur_ptr = cur_ptr->prev_ptr;
	}

	return highest_ptr;
}

int is_new_high(trade_day_info *trade_day_info_ptr, int days_range)
{
	int earliest_date = get_date_by_delta(trade_day_info_ptr->date, days_range);

	trade_day_info *highest_ptr = find_highest_ptr(trade_day_info_ptr, earliest_date);

	if (highest_ptr == NULL)
		return 0; //false

	if (highest_ptr == trade_day_info_ptr)
		return 1; //true

	return 0; //false
}

int is_jump(trade_day_info *trade_day_info_ptr)
{
	if (trade_day_info_ptr->prev_ptr == NULL)
		return 0; //false

	if (trade_day_info_ptr->first > trade_day_info_ptr->prev_ptr->highest)
		return 1; //true

	return 0; //false
}

int has_gap(trade_day_info *trade_day_info_ptr)
{
	if (trade_day_info_ptr->prev_ptr == NULL)
		return 0; //false

	if (trade_day_info_ptr->lowest > trade_day_info_ptr->prev_ptr->highest)
		return 1; //true

	return 0; //false
}

int is_attack(trade_day_info *trade_day_info_ptr, int days_range)
{
	if (trade_day_info_ptr->prev_ptr == NULL)
		return 0; //false

	if (!is_new_high(trade_day_info_ptr->prev_ptr, days_range))
		return 0; //false

	if (has_gap(trade_day_info_ptr))
		return 1; //true

	return 0; //false
}
