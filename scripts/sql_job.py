import mysql.connector, logging

all_data = [[], [], [], [{}], [], []]
# [devices] - [empty] - [Towers] - [Models] - [ips] - [{os}]
users = {}

try:
    conn = mysql.connector.connect(host='localhost', database='roshan', user='root', password='123456')
    if conn.is_connected():
        db_Info = conn.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except:
    print("Error while connecting to MySQL")

def import_devices():
    all_data[0] = []
    cursor.execute('SELECT * FROM devices')
    for row in cursor:
        all_data[0].append({'id': row[0], 'tower_name': row[1], 'device_name': row[2], 'ip': row[3], 'ping': "", 'ptp': row[4], 'models': row[5], 'OS': row[6]})
        all_data[4].insert(0, row[3])

def import_towers():
    all_data[2] = []
    cursor.execute('SELECT * FROM towers')
    for row in cursor:
        all_data[2].append({'id': row[0], 'tower_name': row[1], 'top': row[2], 'left': row[3], 'address': row[4]})

def import_users():
    cursor.execute('SELECT * FROM users')
    for row in cursor:
        users[row[2]] = {'id': row[0], 'rank': row[1], 'username': row[2], 'password': row[3], 'firstname': row[4], 'lastname': row[5]}

def import_models():
    cursor.execute('SELECT * FROM models')
    for row in cursor:
        all_data[3][0][row[1]] = row[2]

def import_logs():
    all_data[1] = []
    cursor.execute('SELECT * FROM log')
    for row in cursor:
        all_data[1].append({'date': row[1], 'event': row[2]})

def insert_tower_name(add_tower_name, address, all_data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO towers (tower_name, top_pos, left_pos, address) VALUES (%s, %s, %s, %s)", (add_tower_name, "200px","200px", address))
    conn.commit()
    import_towers()
    # updates.update_towers(all_data, conn)

def insert_device(radio_name, radio_ip, to_tower, mode, models, os, all_data):
    all_data[0] = []
    cursor = conn.cursor()
    cursor.execute("INSERT INTO devices (tower_name, device_name, ip, ptp, models, os) VALUES (%s, %s, %s, %s, %s, %s)", (to_tower, radio_name, radio_ip, mode, models, os))
    conn.commit()
    import_devices()

def delete_tower_from_sql(delete_tower_name, all_data):
    conn = mysql.connector.connect(host='localhost', database='roshan', user='root', password='123456')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM towers WHERE tower_name = '{delete_tower_name}'")
    conn.commit()
    import_towers()

def delete_model(brand_name):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM type')
    cursor.execute(f" insert into type(type) values ('{brand_name}')")

def delete_device_sql(delete_device_name):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    cursor.execute(f"DELETE FROM devices WHERE [tower_name] in ('{delete_device_name}')")
    conn.commit()
    import_devices()

def edit_tower_name(new_tower_name, target_tower_name):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE towers SET tower_name = '{new_tower_name}' WHERE tower_name = ('{target_tower_name}')")
    cursor.execute(f"UPDATE devices SET tower_name = '{new_tower_name}' WHERE tower_name = ('{target_tower_name}')")
    conn.commit()
    import_towers()
    import_devices()

def insert_model_sql(device_model, device_os):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO models (models, os) VALUES (%s, %s)", (device_model, device_os))
    conn.commit()

def edit_device_name_sql(new_radio_name, target_radio_name,):
    cursor = conn.cursor()
    cursor.execute(f"UPDATE devices SET device_name = '{new_radio_name}' WHERE device_name = ('{target_radio_name}')")
    conn.commit()
    import_devices()

def insert_to_log_sql(dt_string, event):
    cursor = conn.cursor() 
    cursor.execute("INSERT INTO log (date, event) VALUES (%s, %s)", (dt_string, event))
    conn.commit()
    import_models()

def save_move_position(data):
    # conn = mysql.connector.connect(host='localhost', database='roshan', user='root', password='123456')
    # cursor = conn.cursor()
    print(data)
    # u = 0
    # p = 1
    # while True:
        # if len(data) == u:
            # data = []
            # import_towers()
            # break
        # else:
            # cursor.execute(f" UPDATE towers SET top_pos = '{data[u].get('top')}', left_pos = '{data[u].get('left')}' WHERE Id = '{str(p)}'")
            # cursor.execute ("""UPDATE towers SET top_pos=%s, left_pos=%s, WHERE Id=%s""", (data[u].get('top'), data[u].get('left'), data[u].get('id')))
            # p = p + 1
            # u = u + 1
            # conn.commit()

def return_import():
    import_devices()
    import_users()
    import_models()
    import_towers()
    import_logs()
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    return all_data, users