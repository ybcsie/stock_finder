import stock
import os
import datetime


listed_sid_path = "listed.sid"
trade_data_dir = "smd"

months = 25
days_range = 150
new_high_delta_percentage_min = 5
attack_delta_percentage_min = 9


def worker(display_func):
    logger = stock.Logger("work", display_func)
    finish_flag = [False]
    while True:
        updated = True

        logger.logp("update_listed_list : start")
        stock.updater.update_listed_list(listed_sid_path)
        logger.logp("update_listed_list : done\n")

        logger.logp("read_stock_data_cptr_list : start")
        listed_list = stock.reader.read_stock_data_cptr_list(listed_sid_path, months * 30)
        logger.logp("read_stock_data_cptr_list : done\n")

        logger.logp("update_smd_in_list : start")
        stock.updater.update_smd_in_list(listed_list, trade_data_dir, months, finish_flag)
        while not finish_flag[0]:
            stock.tools.delay(5)
        logger.logp("update_smd_in_list : done\n")

        finish_flag[0] = False

        logger.logp("read_trade_data_in_list : start")
        stock.reader.read_trade_data_in_list(trade_data_dir, listed_list, months)
        logger.logp("read_trade_data_in_list : done\n")

        work_arr = stock.init_work_arr(listed_list)

        while True:
            now = datetime.datetime.now()

            if now.hour == 15 and not updated:
                break

            if not updated:
                stock.livedata.get_livedata(listed_list)

            logger.logp("worker : start")

            op_file = open("results.tmp", 'w', encoding="UTF-8")

            op_js = ""
            attack_list = stock.get_attack(work_arr, days_range, attack_delta_percentage_min)
            if len(attack_list) > 0:
                print("\nattack:")
                for stock_id in attack_list:
                    if op_js != "":
                        op_js += ','

                    print(stock_id)
                    op_js += "\"{}\"".format(stock_id)

            op_file.write("var attack = [{}];".format(op_js))
            op_file.flush()

            op_js = ""
            newhigh_list = stock.get_new_high(work_arr, days_range, new_high_delta_percentage_min)
            if len(newhigh_list) > 0:
                print("\nnew high:")
                for stock_id in newhigh_list:
                    if op_js != "":
                        op_js += ','

                    print(stock_id)
                    op_js += "\"{}\"".format(stock_id)

            op_file.write("\nvar newhigh = [{}];".format(op_js))
            op_file.flush()

            op_js = ""
            newhigh_max_list = stock.get_new_high(work_arr, days_range, attack_delta_percentage_min)
            if len(newhigh_max_list) > 0:
                print("\nnew high max:")
                for stock_id in newhigh_max_list:
                    if op_js != "":
                        op_js += ','

                    print(stock_id)
                    op_js += "\"{}\"".format(stock_id)

            op_file.write("\nvar newhigh_max = [{}];".format(op_js))
            op_file.close()
            os.replace("results.tmp", "results.js")

            logger.logp("worker : done")

            if 8 <= now.hour < 14:
                if updated:
                    updated = False
                continue

            logger.logp("sleep 300s ...\n")
            stock.tools.delay(300)

        stock.del_work_arr(work_arr)


if __name__ == '__main__':
    worker(print)
