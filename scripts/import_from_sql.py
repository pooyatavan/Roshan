import pyodbc
import logging

conn = pyodbc.connect("Driver={SQL Server};" "Server=DESKTOP-APD1VGA;" "Database=solar;" "Trusted_connection=yes;")
cursor = conn.cursor()

all_data = [[], [], [], [], []]
# [devices] - [empty] - [Towers] - [type] - [ips]
users = {}

def import_devices():
    cursor.execute('SELECT * FROM solar')
    for row in cursor:
        # make dictionary from all data
        all_data[0].append({'id': row[0], 'tower_name': row[1], 'ap_name': row[2], 'ip': row[3], 'ping': "", 'ptp': row[4], 'models': row[5]})
        all_data[4].insert(0, row[3])

def import_towers():
    cursor.execute('SELECT * FROM tower_name')
    for row in cursor:
        all_data[2].append({'id': row[0], 'tower_name': row[1], 'top': row[2], 'left': row[3], 'address': row[4]})

def import_users():
    cursor.execute('SELECT * FROM users')
    for row in cursor:
        users[row[2]] = {'id': row[0], 'rank': row[1], 'username': row[2], 'password': row[3]}
    

def import_types():
    cursor.execute('SELECT * FROM type')
    for row in cursor:
        all_data[3].append(row[1])
 
def return_import():
    import_devices()
    import_users()
    import_types()
    import_towers()
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    return all_data, users