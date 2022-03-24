import pyodbc

# Update radio list
def update_radios(all_data, conn):
    global stop
    stop = True
    all_data[0] = []
    all_data[4] = []
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solar')
    for row in cursor:
        all_data[0].append({'id': row[0],
                            'tower_name': row[1],
                            'ap_name': row[2],
                            'ip': row[3],
                            'ping': "",
                            'ptp': row[4],
                            'models': row[5]})
        all_data[4].insert(0, row[3])
    stop = False
    return all_data