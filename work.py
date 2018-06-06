import stock
import os


listed_sid_path = "listed.sid"
trade_data_dir = "smd"
months = 25


def worker(display_func):
    logger = stock.Logger("work", display_func)
    finish_flag = [False]
    while True:
        stock.updater.update_listed_list(listed_sid_path)
        listed_list = stock.reader.read_stock_data_cptr_list(listed_sid_path, months * 30)

        stock.updater.update_smd_in_list(listed_list, trade_data_dir, months, finish_flag)

        while not finish_flag[0]:
            stock.tools.delay(5)
            print("waiting")

        finish_flag[0] = False

        stock.reader.read_trade_data_in_list(trade_data_dir, listed_list, months)
        work_arr = stock.init_work_arr(listed_list)

        while True:
            # debug
            break
            # end debug

            stock.livedata.get_livedata(listed_list)

            logger.logp("worker : start")

            op_file = open("results.tmp", 'w', encoding="UTF-8")

            op_js = ""
            attack_list = stock.get_attack(work_arr)
            if len(attack_list) > 0:
                for stock_id in attack_list:
                    if op_js != "":
                        op_js += ','

                    print(stock_id)
                    op_js += "\"{}\"".format(stock_id)

            op_file.write("var attack = [{}];".format(op_js))
            op_file.flush()

            op_js = ""
            newhigh_list = stock.get_new_high(work_arr)
            if len(newhigh_list) > 0:
                for stock_id in newhigh_list:
                    if op_js != "":
                        op_js += ','

                    print(stock_id)
                    op_js += "\"{}\"".format(stock_id)

            op_file.write("\nvar newhigh = [{}];".format(op_js))
            op_file.close()
            os.replace("results.tmp", "results.js")

            logger.logp("worker : done")

            stock.tools.delay(5)

        stock.del_work_arr(work_arr)


if __name__ == '__main__':
    worker(print)
