from . import msgopt, tools
import os
import datetime
import urllib.request
import http.cookiejar
import json


logger = msgopt.Logger("crawler")


def get_listed_list():
    url = "http://isin.twse.com.tw/isin/class_main.jsp?market=1&issuetype=1"
    max_try = 3
    while True:
        if max_try == 0:
            return None
        max_try -= 1

        try:
            res = urllib.request.urlopen(url)
        except:
            logger.logp("Error: get listed id -- urllib")
            continue

        content = res.read().decode("cp950", errors='ignore')
        i_end = content.find("</table>")
        if i_end < 0:
            logger.logp("Error: get listed id -- source")
            continue

        i = i_end + 10

        i_end = content.find("</table>", i)
        if i_end < 0:
            logger.logp("Error: get listed id -- source")
            continue

        op_str = ""
        is_first_data = True

        while i < i_end:
            stock_id_str = ""
            ipo_date = ""

            i = content.find("<tr>", i)
            if i < 0:
                break

            for j in range(3):
                i = content.find("<td", i + 5)

            i = content.find('>', i + 5)
            i += 1

            while content[i] != '<':
                if content[i] != ' ' and content[i] != '\n':
                    stock_id_str += content[i]
                i += 1

            # ipo date
            for j in range(5):
                i = content.find("<td", i + 5)
            i = content.find('>', i + 5)
            i += 1
            while content[i] != '<':
                if content[i] != ' ' and content[i] != '\n':
                    ipo_date += content[i]
                i += 1

            op = "{},{}".format(stock_id_str, ipo_date)
            if is_first_data:
                is_first_data = False
            else:
                op = ';' + op

            op_str += op

        return op_str


def get_month_data(year, month, stock_id):
    logger.logp("Get month data: {} {}".format(year, month))

    arg = "STOCK_DAY?response=json&date={}{:02d}01&stockNo={}".format(year, month, stock_id)
    url = "http://www.twse.com.tw/exchangeReport/" + arg

    tools.delay(3)  # delay

    max_try = 3
    while True:
        logger.logp("Trying connection...")
        from socket import timeout
        try:
            res = urllib.request.urlopen(url, timeout=5)
            logger.logp("OK")

        except timeout:
            logger.logp("Error: urllib -- timeout")
            tools.wait_retry(logger, 10)
            continue

        except :
            logger.logp("Error: urllib")
            tools.wait_retry(logger, 30)
            continue

        logger.logp("Trying json decode...")
        try:
            data = json.loads(res.read().decode())
            if data["stat"] != "OK":
                if data["stat"] == "很抱歉，沒有符合條件的資料!":
                    return []
                logger.logp("data error: stat = {}".format(data["stat"]))

                tools.wait_retry(logger, 5)
                if max_try == 0:
                    return None

                max_try -= 1
                continue

        except:
            logger.logp("Error: json")
            tools.wait_retry(logger, 5)
            continue

        # check content date
        if tools.check_smd_content_by_key(data["data"][0], year * 100 + month):
            return data["data"]

        else:
            logger.logp("error content: {} {}".format(year * 100 + month, data["data"]))
            tools.wait_retry(logger, 5)
            continue