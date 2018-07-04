import stock
import os
import datetime

listed_sid_path = "listed.sid"
trade_data_dir = "smd"
dtd_dir = "dtd"

days_range = 120
months = int(days_range / 20)
new_high_delta_percentage_min = 6
attack_delta_percentage_min = 9

work_arr = None
ready = False


def worker(display_func):
    global work_arr
    global ready

    logger = stock.Logger("work", display_func)
    while True:
        updated = True

        logger.logp("update_listed_list : start")
        stock.updater.update_listed_list(listed_sid_path)
        logger.logp("update_listed_list : done\n")

        stock.updater.update_dtd(dtd_dir)

        logger.logp("read_stock_data_cptr_list : start")
        listed_list = stock.reader.read_stock_data_cptr_list(
            listed_sid_path, months * 30)
        logger.logp("read_stock_data_cptr_list : done\n")

        logger.logp("update_smd_in_list : start")
        force_update = False
        stock.updater.update_smd_in_list(
            listed_list, trade_data_dir, force_update)
        logger.logp("update_smd_in_list : done\n")

        logger.logp("read_trade_data_in_list : start")
        stock.reader.read_trade_data_in_list(
            trade_data_dir, listed_list, months)
        logger.logp("read_trade_data_in_list : done\n")

        now = datetime.datetime.now()
        stock.reader.read_dtd(
            "{}/{}.dtd".format(dtd_dir, now.year * 100 + now.month), listed_list)

        work_arr = stock.init_work_arr(listed_list)
        ready = True

        while True:
            now = datetime.datetime.now()

            if now.hour == 17 and not updated:
                break

            if not updated:
                stock.livedata.get_livedata(listed_list)

            logger.logp("worker : start")

            op_file = open("results/results.tmp", 'w', encoding="UTF-8")

            op_js = ""
            attack_list = stock.utils.get_attack(
                work_arr, days_range, attack_delta_percentage_min)
            if len(attack_list) > 0:
                print("\nattack:")
                for stock_info in attack_list:
                    if op_js != "":
                        op_js += ','

                    stock_id = stock_info[0]
                    if stock_info[1]:
                        day_trading = "(Y)"
                    else:
                        day_trading = "(N)"
                    print(stock_id)
                    op_js += "\"{} {}\"".format(stock_id, day_trading)

            op_file.write("var attack = [{}];".format(op_js))
            op_file.flush()

            op_js = ""
            newhigh_list = stock.utils.get_new_high(
                work_arr, days_range, new_high_delta_percentage_min)
            if len(newhigh_list) > 0:
                print("\nnew high:")
                for stock_info in newhigh_list:
                    if op_js != "":
                        op_js += ','

                    stock_id = stock_info[0]
                    if stock_info[1]:
                        day_trading = "(Y)"
                    else:
                        day_trading = "(N)"
                    print(stock_id)
                    op_js += "\"{} {}\"".format(stock_id, day_trading)

            op_file.write("\nvar newhigh = [{}];".format(op_js))
            op_file.flush()

            op_js = ""
            newhigh_max_list = stock.utils.get_new_high(
                work_arr, days_range, attack_delta_percentage_min)
            if len(newhigh_max_list) > 0:
                print("\nnew high max:")
                for stock_info in newhigh_max_list:
                    if op_js != "":
                        op_js += ','

                    stock_id = stock_info[0]
                    if stock_info[1]:
                        day_trading = "(Y)"
                    else:
                        day_trading = "(N)"
                    print(stock_id)
                    op_js += "\"{} {}\"".format(stock_id, day_trading)

            op_file.write("\nvar newhigh_max = [{}];".format(op_js))
            op_file.close()
            os.replace("results/results.tmp", "results/results.js")

            logger.logp("worker : done")

            if 8 <= now.hour < 14:
                if updated:
                    updated = False
                continue

            logger.logp("sleep 300s ...\n")
            stock.tools.delay(300)

        stock.del_work_arr(work_arr)
        work_arr = None


func_dict = {"attack": stock.utils.get_attack,
             "newhigh": stock.utils.get_new_high}


def get_js(var_name, delta_percentage_min):
    if not ready:
        op_js = "\"preparing data, try later\""

    else:
        if delta_percentage_min is None:
            delta_percentage_min = attack_delta_percentage_min

        op_js = ""
        op_list = func_dict[var_name](
            work_arr, days_range, delta_percentage_min)
        if len(op_list) > 0:
            print("\n{}:".format(var_name))
            for stock_id in op_list:
                if op_js != "":
                    op_js += ','

                print(stock_id)
                op_js += "\"{}\"".format(stock_id)

    return "var {} = ".format(var_name) + "[{}];".format(op_js)


if __name__ == '__main__':
    worker(print)
