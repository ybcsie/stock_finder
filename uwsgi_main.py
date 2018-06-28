import work
import time
import threading
import multiprocessing
import urllib.parse


def application(env, start_response):
    global action_value

    query = env.get("QUERY_STRING")
    path_info = env.get("PATH_INFO")
    uwsgi_location = env.get("UWSGI_LOCATION")
    assert uwsgi_location is not None, "UWSGI_LOCATION is not defined in server setting"

    sub_dir = path_info.split(uwsgi_location + '/')[1]
    work_list = ["attack", "newhigh"]
    op_str = ""

    if sub_dir not in work_list:
        op_str = "{} is not defined".format(sub_dir)
    else:
        query = urllib.parse.parse_qs(query)
        delta_percentage_min_str = query.get("min")
        if delta_percentage_min_str is None:
            delta_percentage_min = None
        else:
            delta_percentage_min = int(delta_percentage_min_str[0])

        op_str += work.get_js(sub_dir, delta_percentage_min)

    start_response("200 OK", [('Content-Type', 'text/html')])
    return [op_str.encode("utf-8")]


logger_thread = None
log_num = 500
msg_list = [None] * log_num
last_msg_idx = -1

action_value = multiprocessing.Value('i', 0)


def logger():
    while True:
        time.sleep(0.5)
        cur_msg_idx = last_msg_idx
        if cur_msg_idx == -1:
            continue

        cur_msg_idx_bak = cur_msg_idx
        opmsg = ""

        while True:
            cur_msg_idx += 1
            if cur_msg_idx > log_num - 1:
                cur_msg_idx = 0

            if msg_list[cur_msg_idx] is None:
                cur_msg_idx = 0

            opmsg += "+{}".format(msg_list[cur_msg_idx])
            if cur_msg_idx == cur_msg_idx_bak:
                break

        f = open("data.js", 'w')
        f.write("var data = \"\" {};".format(opmsg))
        f.close()


def op(msg):
    print(msg)

    global logger_thread
    global msg_list
    global last_msg_idx

    if logger_thread is None:
        logger_thread = threading.Thread(target=logger)
        logger_thread.start()

    last_msg_idx += 1
    if last_msg_idx > log_num - 1:
        last_msg_idx = 0

    msg_list[last_msg_idx] = "\"{}\n\"".format(msg).replace('\n', "<br/>")


if __name__ == '__main__':
    pass

else:
    threading.Thread(target=work.worker, args=(op,)).start()
