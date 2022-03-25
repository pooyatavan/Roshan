from multiprocessing.dummy import Pool as ThreadPool
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import pyodbc
from pythonping import ping
import time
import threading
from waitress import serve
from scripts import import_from_sql
from scripts import RPR
from scripts import SD
from scripts import UR
from scripts import User_LRCHR

pool = ThreadPool(3)
conn = pyodbc.connect("Driver={SQL Server};" "Server=DESKTOP-APD1VGA;" "Database=solar;" "Trusted_connection=yes;")
ping_data = []
time_refresh = 10
data = []
add_temp = []
stop = False
username = ""
all_devices = 0
currency_number = []

all_data, users = import_from_sql.return_import()

# Create tower
def create_tower(add_tower_name):
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
            update_towers()
            break
        else:
            q = q + 1

# Add radio to list
def add_radio():
    global stop
    stop = True
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
            cursor.execute(f" insert into solar(id, name, access_point, ip, ptp, models) values ('{q}' "
                           f",'{add_temp[0].get('tower_name')}',"
                           f" '{add_temp[0].get('radio_name')}',"
                           f" '{add_temp[0].get('radio_ip')}',"
                           f" '{add_temp[0].get('mode')}',"
                           f" '{add_temp[0].get('models')}')")
            conn.commit()
            add_temp = []
            stop = False
            UR.update_radios(all_data, conn)
            break
        else:
            q = q + 1

# Delete tower
def delete_tower(delete_tower_name):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tower_name')
    cursor.execute(f"DELETE FROM tower_name WHERE [tower_name] in ('{delete_tower_name}')")
    conn.commit()
    update_towers()

# Edit tower name
def edit_tower_name(target, new):
    global stop
    stop = True
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solar')
    cursor.execute(f"UPDATE tower_name SET tower_name = '{new}' WHERE tower_name = ('{target}')")
    cursor.execute(f"UPDATE solar SET name = '{new}' WHERE name = ('{target}')")
    conn.commit()
    update_towers()
    stop = False
    UR.update_radios(all_data, conn)

# Update tower position
def update_tower_position(data):
    u = 0
    p = 1
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tower_name')
    while True:
        if len(data) == u:
            data = []
            update_towers()
            break
        else:
            cursor.execute(f" UPDATE tower_name SET top_pos = '{data[u].get('top')}',"
                           f" left_pos = '{data[u].get('left')}' WHERE Id = {str(p)} ")
            p = p + 1
            u = u + 1
            conn.commit()

# Update towers list
def update_towers():
    temp = []
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tower_name')
    for row in cursor:
        temp.append({'id': row[0], 'tower_name': row[1], 'top': row[2], 'left': row[3]})
    all_data[2] = []
    all_data[2] = temp

# Ping calc
def ping_system(ip):
    if stop is False:
        result = ping(ip, size=1, count=1)
        if result.rtt_avg_ms == 2000:
            ping_data.append({'ip': ip, 'ping': "Request timeout"})
        else:
            ping_data.append({'ip': ip, 'ping': result.rtt_avg_ms})

# Edit radio name
def edit_radio_name(new, target):
    global stop
    stop = True
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solar')
    cursor.execute(f"UPDATE solar SET access_point = '{new}' WHERE access_point = ('{target}')")
    conn.commit()
    update_towers()
    stop = False
    all_data = UR.update_radios(all_data, conn)

# Add brand
def add_brand(brand_name):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM type')
    cursor.execute(f" insert into type(type) values ('{brand_name}')")
    all_data[3] = []
    cursor.execute('SELECT * FROM type')
    for row in cursor:
        all_data[3].append(row[1])
    conn.commit()

# start flask server
def flask():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.secret_key = "hi"

    # Data pass through
    @app.route('/_stuff', methods=['GET', 'Post'])
    def stuff():
        if request.method == 'POST':
            data = []
            data = request.get_json()
            update_tower_position(data)
        return jsonify(alldata=all_data)

    # Login
    @app.route("/", methods=['GET', 'POST'], )
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            login_result = User_LRCHR.user_login(users, username, password)
            if login_result == False:
                error = 'You have entered an invalid username or password'
            else:
                session["username"] = username
                return redirect(url_for('solar'))
        else:
            if "username" in session:
                return redirect(url_for('solar'))
        return render_template('login.html', error=error, alldata=all_data)

    # Solar page
    @app.route("/solar")
    def solar():
        global username
        if "username" in session:
            username = session["username"]
            return render_template('solar.html', alldata=all_data, username=username)
        else:
            return redirect(url_for('login'))

    # logout page
    @app.route("/logout")
    def logout():
        session.pop("username", None)
        return redirect(url_for('login'))

    # Move
    @app.route("/move", methods=['POST', 'GET'])
    def move():
        global username
        if "username" in session:
            username = session["username"]
            username_ch = session["username"]
            # check username rank for access this page
            if User_LRCHR.check_rank(username_ch, users) == True:
                return render_template('move.html', username=username)
            else:
                return render_template('denied.html', username=username)
        else:
            return redirect(url_for('login'))

    # Dashboard
    @app.route("/dashboard", methods=['POST', 'GET'])
    def dashboard():
        global username
        global all_devices
        if "username" in session:
            username = session["username"]
            all_devices = len(all_data[0])
            all_towers =  len(all_data[2])
            return render_template('dashboard.html', username=username, all_devices=all_devices, all_towers=all_towers, currency_number=currency_number)
        else:
            return redirect(url_for('login'))

    # Add
    @app.route("/add", methods=['POST', 'GET'])
    def add():
        error = None
        global username
        # Add tower
        if request.method == 'POST':
            if request.form['submit'] == 'Add Tower':
                tower_name = request.form['tower_name']
                if tower_name == "":
                    error = 'Empty - Choose a name for your tower'
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    i = 0
                    while len(all_data[2]) > i:
                        if all_data[2][i]['tower_name'] == tower_name:
                            error = f'{tower_name} is all ready exist'
                            return render_template('add.html', error=error, all_data=all_data, username=username)
                        else:
                            i = i + 1
                    if i == len(all_data[2]):
                        create_tower(tower_name)
                        error = f'{tower_name} added successfully'
                        return render_template('add.html', error=error, all_data=all_data, username=username)

            # Add radio
            if request.form['submit'] == 'Add Radio':
                radio_name = request.form['radio_name']
                radio_ip = request.form['radio_ip']
                tower_name = request.form['tower_name']
                mode = request.form['mode']
                models = request.form['models']
                if "" in (radio_name, radio_ip, tower_name, mode, models):
                    error = 'One of these fields are empty'
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    add_temp.append(
                        {'tower_name': tower_name, 'radio_name': radio_name, 'radio_ip': radio_ip, 'mode': mode,
                         'models': models})
                    add_radio()
                    error = f'{radio_name} in tower {tower_name} with ip {radio_ip} added successfully'
                    return render_template('add.html', error=error, all_data=all_data, username=username)

            # delete tower name
            if request.form['submit'] == 'Delete Tower':
                delete_tower_name = ""
                delete_tower_name = request.form['delete']
                if "None" in delete_tower_name:
                    error = "Choose a tower"
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    error = f"{delete_tower_name} Successfully deleted"
                    delete_tower(delete_tower_name)
                    return render_template('add.html', error=error, all_data=all_data, username=username)

            # Edit tower name
            if request.form['submit'] == 'Change tower name':
                target_tower_name = request.form['target_tower_name']
                new_tower_name = request.form['new_tower_name']
                if new_tower_name == "":
                    error = "Choose a new name for your tower"
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    i = 0
                    while len(all_data[2]) > i:
                        if all_data[2][i]['tower_name'] == new_tower_name:
                            error = f'{new_tower_name} is all ready exist'
                            return render_template('add.html', error=error, all_data=all_data, username=username)
                        else:
                            i = i + 1
                    if i == len(all_data[2]):
                        error = f"Successfully changed from {target_tower_name} to {new_tower_name}"
                        edit_tower_name(target_tower_name, new_tower_name)
                        return render_template('add.html', error=error, all_data=all_data, username=username)

            # Edit device name
            if request.form['submit'] == 'Change radio name':
                target_radio_name = request.form['target_radio_name']
                new_radio_name = request.form['new_radio_name']
                if new_radio_name == "":
                    error = "Choose a new name for your radio"
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    i = 0
                    while len(all_data[0]) > i:
                        if all_data[0][i]['ap_name'] == new_radio_name:
                            error = f'{new_radio_name} is all ready exist'
                            return render_template('add.html', error=error, all_data=all_data, username=username)
                        else:
                            i = i + 1
                    if i == len(all_data[0]):
                        error = f"Successfully changed from {target_radio_name} to {new_radio_name}"
                        edit_radio_name(new_radio_name, target_radio_name)
                        return render_template('add.html', error=error, all_data=all_data, username=username)

            # Add brand
            if request.form['submit'] == 'add radio type':
                radio_type = request.form['radio_type']
                if radio_type == "":
                    error = "Type a radio type name"
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    error = "done"
                    add_brand(radio_type)
                    return render_template('add.html', error=error, all_data=all_data, username=username)

            # Register user
            if request.form['submit'] == 'REGISTER':
                rank = request.form['rank']
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                new_username = request.form['new_username']
                new_password = request.form['new_password']
                if firstname == "" or lastname == "" or new_username == "" or new_password == "":
                    error = "one of the field are empty"
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    error, refresh_users_list = User_LRCHR.user_check(rank, firstname, lastname, new_username, new_password, users, conn)
                    users = refresh_users_list
                    return render_template('add.html', error=error, all_data=all_data, username=username)

        else:
            if "username" in session:
                username = session["username"] = session["username"]
                username_ch = session["username"]
                # check username rank for access this page
                if User_LRCHR.check_rank(username_ch, users) == True:
                    return render_template('add.html', username=username, all_data=all_data, error=error)
                else:
                    return render_template('denied.html', username=username)
            else:
                return redirect(url_for('login'))

    if __name__ == '__main__':
        serve(app, host="0.0.0.0", port=80)
        # app.run(debug=False, host='0.0.0.0', port=80)

# flask start thread section
flask_thread = threading.Thread(target=flask)
flask_thread.start()

# refresh loop
while True:
    time.sleep(time_refresh)
    results = pool.map(ping_system, all_data[4])
    all_data[0] = RPR.replace(stop, ping_data, all_data)
    all_data[0] = SD.sort_data(all_data)
    ping_data.clear()
    # currency()