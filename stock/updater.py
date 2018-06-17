from . import crawler, msgopt, tools
from .c_api import stock
import json
import datetime
import threading
import os


logger = msgopt.Logger("updater")


def update_listed_list(listed_path):
    content = crawler.get_listed_list()
    if content is None:
        logger.logp("cannot get listed list")
        return -1

    sid_file = open(listed_path, 'w', encoding="UTF-8")
    sid_file.write(content)
    sid_file.close()
    return 0


def get_exist_smd_dict(smd_path):
    opt = {}
    if not os.path.exists(smd_path):
        return opt

    try:
        smd_file = open(smd_path, 'r')

        for key, content in json.loads(smd_file.read()).items():
            if len(content) == 0 or tools.check_smd_content_by_key(content[0], key):
                opt[key] = content

        smd_file.close()

        return opt

    except:
        return opt


def is_content_need_update(content):
    if content is None:
        return True

    if len(content) == 0:
        return False

    now = datetime.datetime.now()
    if tools.check_smd_content_by_key(content[0], int(now.strftime("%Y%m"))):
        if int(now.strftime("%Y%m%d")) > tools.tw_date2int(content[len(content) - 1][0]):
            return True

    return False


def update_smd(smd_path, stock_id, months):
    exist_dict = get_exist_smd_dict(smd_path)

    now = datetime.datetime.now()
    cur_month = now.month
    cur_year = now.year
    for i in range(months):
        if cur_month == 0:
            cur_month = 12
            cur_year -= 1

        key = "{}{:02d}".format(cur_year, cur_month)
        content = exist_dict.get(key)

        if is_content_need_update(content):
            content = crawler.get_month_data(cur_year, cur_month, stock_id)

            if content is None:
                logger.logp("cannot get data: {} {} {}".format(
                    cur_year, cur_month, stock_id))
            else:
                exist_dict[key] = content

        cur_month -= 1

    smd_tmp_path = "{}.tmp".format(smd_path)
    smd_tmp_file = open(smd_tmp_path, 'w', encoding="UTF-8")
    smd_tmp_file.write(json.dumps(exist_dict))
    smd_tmp_file.close()

    os.replace(smd_tmp_path, smd_path)


def require_update(update_log_path):
    if not os.path.exists(update_log_path):
        return True

    log_file = open(update_log_path, 'r', encoding="UTF-8")
    last_datetime = datetime.datetime.strptime(log_file.read(), "%Y/%m/%d/%H")
    log_file.close()
    now = datetime.datetime.now()

    update_datetime = datetime.datetime.strptime(
        "{}/{}/{}/15".format(now.year, now.month, now.day), "%Y/%m/%d/%H")
    if now.hour < 15:
        update_datetime -= datetime.timedelta(days=1)

    if last_datetime >= update_datetime:
        return False

    return True


def t_update_smd_in_list(stock_data_cptr_list, smd_dir, months, finish_flag, force_update):
    update_log_path = smd_dir + "/update.log"

    if require_update(update_log_path) or force_update:
        for stock_data_cptr in stock_data_cptr_list:
            stock_id = stock.get_stock_id(stock_data_cptr)
            smd_path = "{}/{}.smd".format(smd_dir, stock_id)

            logger.logp("update {}".format(stock_id))
            update_smd(smd_path, stock_id, months)

    update_log_file = open(update_log_path, 'w')
    update_log_file.write(datetime.datetime.now().strftime("%Y/%m/%d/%H"))
    update_log_file.close()

    finish_flag[0] = True


def update_smd_in_list(stock_data_cptr_list, smd_dir, months, finish_flag, force_update=False):
    threading.Thread(target=t_update_smd_in_list, args=(
        stock_data_cptr_list, smd_dir, months, finish_flag, force_update)).start()


def get_exist_dtd_dict(dtd_path):
    if not os.path.exists(dtd_path):
        return {}

    try:
        dtd_file = open(dtd_path, 'r')

        opt = json.loads(dtd_file.read())

        dtd_file.close()

        return opt

    except:
        return {}


def update_month_dtd(dtd_path, yyyymm):
    if yyyymm < 201401:
        return

    now = datetime.datetime.now()
    cur_datetime = datetime.datetime.strptime("{}01".format(yyyymm), "%Y%m%d")
    one_day_delta = datetime.timedelta(days=1)

    exist_dict = get_exist_dtd_dict(dtd_path)
    while True:
        if cur_datetime > now or int(cur_datetime.strftime("%Y%m")) > yyyymm:
            break

        if cur_datetime >= datetime.datetime.strptime("20140106", "%Y%m%d"):
            key = "{}".format(cur_datetime.strftime("%Y%m%d"))
            content = exist_dict.get(key)

            if content is None:
                content = crawler.get_day_trading_data(key)

                if content is None:
                    logger.logp("cannot get data: {}".format(key))
                else:
                    exist_dict[key] = content

        cur_datetime += one_day_delta

    dtd_tmp_path = "{}.tmp".format(dtd_path)
    dtd_tmp_file = open(dtd_tmp_path, 'w', encoding="UTF-8")
    dtd_tmp_file.write(json.dumps(exist_dict))
    dtd_tmp_file.close()

    os.replace(dtd_tmp_path, dtd_path)


def update_dtd(dtd_dir, months):
    now = datetime.datetime.now()
    cur_month = now.month
    cur_year = now.year
    for i in range(months):
        if cur_month == 0:
            cur_month = 12
            cur_year -= 1

        yyyymm = cur_year * 100 + cur_month
        update_month_dtd("{}/{}.dtd".format(dtd_dir, yyyymm), yyyymm)

        cur_month -= 1
