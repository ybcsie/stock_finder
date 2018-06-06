#ifndef STOCK_DATA_H
#define STOCK_DATA_H

#define STOCK_ID_LEN 4
#define DATE_LEN 8
#define FORMATTED_DATE_LEN DATE_LEN + 2

typedef struct trade_day_info trade_day_info;
struct trade_day_info
{
	trade_day_info *prev_ptr;
	trade_day_info *next_ptr;

	int date; //20180101
	float vol;
	float first;
	float highest;
	float lowest;
	float last;
	float delta;
};

typedef struct
{
	trade_day_info *head_ptr;
	trade_day_info *tail_ptr;
	int list_len;

} trade_day_info_dllist;

typedef struct
{
	int stock_id;
	int ipo_date; //20180101
	trade_day_info_dllist *trade_day_info_list_ptr;

} stock_data;

typedef struct
{
	stock_data **ptr_arr;
	int *cur_len_ptr;
	int size;

} stock_data_arr;

trade_day_info_dllist *new_trade_day_info_dllist_ptr();

void add_trade_day_info_new_node(stock_data *stock_data_ptr, int date, float vol, float first, float highest, float lowest, float last, float delta);
void update_trade_day_info_last_node(stock_data *stock_data_ptr, int date, float vol, float first, float highest, float lowest, float last, float delta);

int is_new_high(trade_day_info *trade_day_info_ptr, int days_range);
int is_jump(trade_day_info *trade_day_info_ptr);
int has_gap(trade_day_info *trade_day_info_ptr);
int is_attack(trade_day_info *trade_day_info_ptr, int days_range);

#endif