from .c_api import stock
from . import utils
import matplotlib.pyplot as plt
import datetime


def plot(work_arr, days_range, attack_delta_percentage_min, buy_rule_no, roi_rule_no):
    plt.figure(figsize=(16, 9))
    plt.ylabel("Return on Investment per Month (%)")
    plt.xlabel("Max Profit per Target (%)")
    plt.grid(True)

    days = 20
    while True:
        if days > 600:
            break

        x = []
        y = []

        percentage = 1

        while True:
            if percentage >= 9:
                break

            x.append(percentage)
            y.append(
                utils.cal_p(work_arr, days_range, attack_delta_percentage_min, days, percentage, buy_rule_no, roi_rule_no) / days * 20)
            percentage += 0.5

        plt.plot(x, y, label="{} days".format(days), linewidth=1)

        days += 20

    plt.legend()
    plt.savefig("imgopt/{}.png".format(days))
    plt.close()


def plot_days(work_arr, days_range, attack_delta_percentage_min, days, buy_rule_no, roi_rule_no):
    figure_name = "ROI_day"

    percentage = 3

    while True:
        if percentage > 5:
            break

        plt.figure(figsize=(16, 9))
        plt.ylabel("Return on Investment per Month (%)")
        plt.xlabel("Day")
        plt.grid(True)

        x = []
        y = []

        cur_datetime = datetime.datetime.now()

        for i in range(days):
            date = int(cur_datetime.strftime("%Y%m%d"))
            cur_datetime -= datetime.timedelta(days=1)
            er = utils.cal_day_e(work_arr, days_range, attack_delta_percentage_min, date, percentage, buy_rule_no, roi_rule_no)

            if er == -99999:
                continue

            x.append(i)
            y.append(er)

        plt.plot(x, y, label="{} %".format(percentage), linewidth=1)
        plt.legend()
        plt.savefig("imgopt/{}_{}.png".format(figure_name, percentage))
        plt.close()

        percentage += 0.5


def plot_months(work_arr, days_range, attack_delta_percentage_min, months, buy_rule_no, roi_rule_no):
    figure_name = "ROI_month"
    percentage = 2
    now = datetime.datetime.now()

    plt.figure(figsize=(16, 9))
    plt.ylabel("Return on Investment (%)")
    plt.xlabel("Month")
    plt.grid(True)

    while True:
        x = []
        x_str = []
        y = []

        x_avg = []
        y_avg = []

        if percentage > 4:
            break
        cur_month = now.month
        cur_year = now.year

        for i in range(months):
            if cur_month == 0:
                cur_month = 12
                cur_year -= 1

            yyyymm = int("{}{:02d}".format(cur_year, cur_month))
            er = utils.cal_month_e(work_arr, days_range, attack_delta_percentage_min, yyyymm, percentage, buy_rule_no, roi_rule_no)
            if er == -99999:
                print("no target : {}".format(yyyymm))
                continue

            x.append(months - i)
            y.append(er)

            if i % 10:
                x_str.append("")
            else:
                x_str.append(yyyymm)

            if (not i % 3) and i > 0:
                y_avg.append((y[i] + y[i - 1] + y[i - 2]) / 3)
                x_avg.append(months - i)

            cur_month -= 1

        # plt.plot(x, y, "o")
        plt.plot(x, y, label="{}%".format(percentage), linewidth=1)
        plt.plot(x_avg, y_avg, label="{}% 3 Months MA".format(percentage), linewidth=0.3)
        plt.xticks(x, x_str)
        percentage += 0.5

    plt.legend()
    plt.savefig("imgopt/{}_{}.png".format(figure_name, months))
    plt.close()


def plot_months_percentage(work_arr, days_range, attack_delta_percentage_min, months, buy_rule_no, roi_rule_no):
    figure_name = "ROI_MPPT"
    now = datetime.datetime.now()

    plt.figure(figsize=(16, 9))
    plt.ylabel("Return on Investment (%)")
    plt.xlabel("Max Profit per Target (%)")
    plt.grid(True)

    cur_month = now.month
    cur_year = now.year

    e_max_x = []
    e_max_y = []

    for i in range(months):
        if cur_month == 0:
            plt.plot(e_max_x, e_max_y, "ko", label="Max")
            e_max_x = []
            e_max_y = []
            plt.legend()
            plt.savefig("imgopt/{}_{}.png".format(figure_name, cur_year))
            plt.close()
            plt.figure(figsize=(16, 9))
            plt.ylabel("Return on Investment (%)")
            plt.xlabel("Max Profit per Target (%)")
            plt.grid(True)

            cur_month = 12
            cur_year -= 1

        yyyymm = int("{}{:02d}".format(cur_year, cur_month))
        percentage = 1

        x = []
        y = []

        e_max_xy = [0, 0]
        while True:
            if percentage >= 9:
                break

            er = utils.cal_month_e(work_arr, days_range, attack_delta_percentage_min, yyyymm, percentage, buy_rule_no, roi_rule_no)
            percentage += 0.5

            if er == -99999:
                print("no target : {}".format(yyyymm))
                continue

            x.append(percentage)
            y.append(er)
            if er > e_max_xy[1]:
                e_max_xy = [percentage, er]

        plt.plot(x, y, label="{}".format(yyyymm), linewidth=1)

        e_max_x.append(e_max_xy[0])
        e_max_y.append(e_max_xy[1])

        cur_month -= 1

    plt.plot(e_max_x, e_max_y, "ko", label="Max")
    plt.legend()
    plt.savefig("imgopt/{}_{}.png".format(figure_name, cur_year))
    plt.close()


def plot_3months_percentage(work_arr, days_range, attack_delta_percentage_min, months, buy_rule_no, roi_rule_no):
    figure_name = "ROI_MPPT_3M_AVG"
    now = datetime.datetime.now()

    plt.figure(figsize=(16, 9))
    plt.ylabel("Return on Investment per Month (%)")
    plt.xlabel("Max Profit per Target (%)")
    plt.grid(True)

    cur_month = now.month
    cur_year = now.year

    e_max_x = []
    e_max_y = []

    x = []
    y_each_month = []
    yyyymm_list = []

    for i in range(months):
        if cur_month == 0:
            plt.plot(e_max_x, e_max_y, "ko", label="Max")
            e_max_x = []
            e_max_y = []
            plt.legend()
            plt.savefig("imgopt/{}_{}.png".format(figure_name, cur_year))
            plt.close()

            plt.figure(figsize=(16, 9))
            plt.ylabel("Return on Investment per Month (%)")
            plt.xlabel("Max Profit per Target (%)")
            plt.grid(True)

            cur_month = 12
            cur_year -= 1

        yyyymm_list.append(int("{}{:02d}".format(cur_year, cur_month)))
        percentage = 3

        y_each_month.append([])

        while True:
            if percentage >= 6:
                break

            er = utils.cal_month_e(work_arr, days_range, attack_delta_percentage_min, yyyymm_list[i], percentage, buy_rule_no, roi_rule_no)
            percentage += 0.5

            if er == -99999:
                break

            if i == 0:
                x.append(percentage)

            y_each_month[i].append(er)

        if len(y_each_month[i]) == 0:
            break

        if i >= 2:
            y = []
            e_max_xy = [0, 0]
            for x_idx, x_val in enumerate(x):
                cur_e = (y_each_month[i][x_idx] + y_each_month[i - 1][x_idx] + y_each_month[i - 2][x_idx]) / 3
                y.append(cur_e)
                if cur_e > e_max_xy[1]:
                    e_max_xy = [x_val, cur_e]

            plt.plot(x, y, label="{} ~ {}".format(yyyymm_list[i], yyyymm_list[i - 2]), linewidth=1)
            e_max_x.append(e_max_xy[0])
            e_max_y.append(e_max_xy[1])

        cur_month -= 1

    plt.plot(e_max_x, e_max_y, "ko", label="Max")
    plt.legend()
    plt.savefig("imgopt/{}_{}.png".format(figure_name, cur_year))
    plt.close()
