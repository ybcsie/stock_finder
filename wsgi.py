import work
import time
import threading
import multiprocessing
import urllib.parse


def application(env, start_response):
    global action_value

    try:
        query = env["QUERY_STRING"]
    except:
        query = ""
    op_str = "OK <br/>{}<br/>".format(env)
    query = urllib.parse.parse_qs(query)
    action = int(query.get("action", [0])[0])

    action_value.value = action

    op_str += "OK <br/><br/> {}".format(action)

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
    multiprocessing.Process(target=work.worker, args=(op,)).start()

