from scripts import log

# Update towers list
def update_towers(all_data, conn):
    temp = []
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tower_name')
    for row in cursor:
        temp.append({'id': row[0], 'tower_name': row[1], 'top': row[2], 'left': row[3]})
    all_data[2] = []
    all_data[2] = temp
    return all_data

# Create tower after check
def create_tower(add_tower_name, conn, all_data):
    check = []
    h = 0
    q = 1
    while True:
        if len(all_data[2]) == h:
            break
        else:
            check.append(all_data[2][h].get('id'))
            h = h + 1
    while True:
        if q not in check:
            cursor = conn.cursor() 
            cursor.execute('SELECT * FROM tower_name')
            cursor.execute(f" insert into tower_name(id, tower_name, top_pos, left_pos) values ('{q}', '{str(add_tower_name)}', '200px', '200px')")
            conn.commit()
            update_towers(all_data, conn)
            event = f"Tower {add_tower_name} was added"
            log.in_to_the_log(conn, event)
            break
        else:
            q = q + 1

#check tower if allready exist
def check_tower_name(all_data, tower_name, conn):
    i = 0
    while len(all_data[2]) > i:
        if all_data[2][i]['tower_name'] == tower_name:
            return f'{tower_name} is all ready exist'
        else:
            i = i + 1
    if i == len(all_data[2]):
        create_tower(tower_name, conn, all_data)
        return f'{tower_name} added successfully'

# Update tower position
def update_tower_position(data, conn, all_data):
    u = 0
    p = 1
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tower_name')
    while True:
        if len(data) == u:
            data = []
            update_towers(all_data, conn)
            break
        else:
            cursor.execute(f" UPDATE tower_name SET top_pos = '{data[u].get('top')}',"
                           f" left_pos = '{data[u].get('left')}' WHERE Id = {str(p)} ")
            p = p + 1
            u = u + 1
            conn.commit()

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

# Delete device name
def delete_device(delete_device_name, conn, all_data):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solar')
    cursor.execute(f"DELETE FROM solar WHERE [access_point] in ('{delete_device_name}')")
    conn.commit()
    update_radios(all_data, conn)
    event = f"Device {delete_device_name} was deleted"
    log.in_to_the_log(conn, event)

# Edit tower name
def edit_tower_name(target_tower_name, new_tower_name, conn, all_data):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solar')
    cursor.execute(f"UPDATE tower_name SET tower_name = '{new_tower_name}' WHERE tower_name = ('{target_tower_name}')")
    cursor.execute(f"UPDATE solar SET name = '{new_tower_name}' WHERE name = ('{target_tower_name}')")
    conn.commit()
    update_towers(all_data, conn)
    update_radios(all_data, conn)
    event = f"Tower name from {target_tower_name} to {new_tower_name} has changed"
    log.in_to_the_log(conn, event)

# Add radio
def add_radio(radio_name, radio_ip, to_tower, mode, models, conn, all_data):
    check = []
    h = 0
    q = 0
    global add_temp
    while True:
        if len(all_data[0]) == h:
            break
        else:
            check.append(all_data[0][h].get('id'))
            h = h + 1
    while True:
        if q not in check:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM solar')
            cursor.execute(f" insert into solar(id, name, access_point, ip, ptp, models) values ('{q}', '{to_tower}', '{radio_name}', '{radio_ip}', '{mode}', '{models}')")
            conn.commit()
            update_radios(all_data, conn)
            event = f"Device {radio_name} added"
            log.in_to_the_log(conn, event)
            break
        else:
            q = q + 1

# Delete tower
def delete_tower(delete_tower_name, conn, all_data):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tower_name')
    cursor.execute(f"DELETE FROM tower_name WHERE [tower_name] in ('{delete_tower_name}')")
    conn.commit()
    update_towers(all_data, conn)
    event = f"Tower {delete_tower_name} deleted"
    log.in_to_the_log(conn, event)

# Add brand
def add_brand(brand_name, all_data, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM type')
    cursor.execute(f" insert into type(type) values ('{brand_name}')")
    all_data[3] = []
    cursor.execute('SELECT * FROM type')
    for row in cursor:
        all_data[3].append(row[1])
    conn.commit()
    event = f"Radio model {brand_name} added"
    log.in_to_the_log(conn, event)

# Edit radio name
def edit_radio_name(new_radio_name, target_radio_name, conn, all_data):
    global stop
    stop = True
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solar')
    cursor.execute(f"UPDATE solar SET access_point = '{new_radio_name}' WHERE access_point = ('{target_radio_name}')")
    conn.commit()
    update_radios(all_data, conn)
    event = f"Radio name changed from {target_radio_name} to {new_radio_name} "
    log.in_to_the_log(conn, event)
