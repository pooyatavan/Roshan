from operator import itemgetter

# Sort all_data by Access points names
def sort_data(all_data):
    all_data[0].sort(key=itemgetter('ap_name'))
    return all_data[0]