import time

timeout_list = []


# Insert ping ms in to the list all_data
def replace(stop, ping_data, all_data):
    counter = 0
    if stop is False:
        while counter < len(ping_data):
            finder = next((index for (index, d) in enumerate(all_data[0]) if d["ip"] == ping_data[counter]["ip"]), None)
            if ping_data[counter]["ping"] == "Request timeout":
                fto_insert(ping_data, counter, all_data, finder, timeout_list)
            else:
                all_data[0][finder]['ping'] = ping_data[counter]["ping"]
                fto_remove(ping_data, counter, timeout_list)
            counter = counter + 1
    return all_data[0]


# insert in timeout dict
def fto_insert(ping_data, counter, all_data, finder, timeout_list):
    if not timeout_list:
        tto = time.gmtime()
        tto = f'{tto[3]}{tto[4]}{tto[5]}'
        timeout_list.append({'ip': ping_data[counter]["ip"], 'time': tto})
    else:
        t = 0
        while True:
            if len(timeout_list) == t:
                tto = time.gmtime()
                tto = f'{tto[3]}{tto[4]}{tto[5]}'
                timeout_list.append({'ip': ping_data[counter]["ip"], 'time': tto})
                break
            elif ping_data[counter]['ip'] == timeout_list[t]['ip']:
                tto = time.gmtime()
                tto = f'{tto[3]}{tto[4]}{tto[5]}'
                calc_time = int(tto) - (int(timeout_list[t]['time']))
                if calc_time > 150:
                    all_data[0][finder]['ping'] = "Request timeout"
                break
            else:
                t = t + 1


# remove from timeout_list
def fto_remove(ping_data, counter, timeout_list):
    y = 0
    while True:
        if y >= len(timeout_list):
            break
        else:
            if ping_data[counter]['ip'] == timeout_list[y]['ip']:
                timeout_list.remove(timeout_list[y])
                break
            else:
                y = y + 1