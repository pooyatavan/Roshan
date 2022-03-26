from multiprocessing.dummy import Pool as ThreadPool
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import pyodbc
from pythonping import ping
import time
import threading
from waitress import serve
from scripts import import_from_sql, log, RPR, User_LRCHR, panel, sort_data_by_name

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

# Ping calc
def ping_system(ip):
    if stop is False:
        result = ping(ip, size=1, count=1)
        if result.rtt_avg_ms == 2000:
            ping_data.append({'ip': ip, 'ping': "Request timeout"})
        else:
            ping_data.append({'ip': ip, 'ping': result.rtt_avg_ms})


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
            panel.update_tower_position(data, conn, all_data)
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
            print(users)
            username = session["username"]
            all_devices = len(all_data[0])
            all_towers =  len(all_data[2])
            return render_template('dashboard.html', username=username, all_devices=all_devices, all_towers=all_towers, currency_number=currency_number)
        else:
            return redirect(url_for('login'))

    # Log
    @app.route("/log", methods=['POST', 'GET'])
    def log():
        if "username" in session:
            username = session["username"]
            return render_template('log.html', username=username)
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
                    error = panel.check_tower_name(all_data, tower_name, conn)
                    return render_template('add.html', error=error, all_data=all_data, username=username)

            # Add radio
            if request.form['submit'] == 'ADD DEVICE':
                radio_name = request.form['radio_name']
                radio_ip = request.form['radio_ip']
                to_tower = request.form['tower_name']
                mode = request.form['mode']
                models = request.form['models']
                if "" in (radio_name, radio_ip, to_tower, mode, models):
                    error = 'One of these fields are empty'
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    panel.add_radio(radio_name, radio_ip, to_tower, mode, models, conn, all_data)
                    error = f'{radio_name} in tower {to_tower} with ip {radio_ip} added successfully'
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
                    panel.delete_tower(delete_tower_name, conn, all_data)
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
                        panel.edit_tower_name(target_tower_name, new_tower_name, conn, all_data)
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
                        panel.edit_radio_name(new_radio_name, target_radio_name, conn, all_data)
                        return render_template('add.html', error=error, all_data=all_data, username=username)

            # Add brand
            if request.form['submit'] == 'add radio type':
                radio_type = request.form['radio_type']
                if radio_type == "":
                    error = "Type a radio type name"
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    error = "done"
                    panel.add_brand(radio_type, all_data, conn)
                    return render_template('add.html', error=error, all_data=all_data, username=username)

            # delete device name
            if request.form['submit'] == 'Delete device name':
                delete_device_name = ""
                delete_device_name = request.form['target_device_name']
                if "None" in delete_device_name:
                    error = "Choose a tower"
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    error = f"{delete_device_name} Successfully deleted"
                    panel.delete_device(delete_device_name, conn, all_data)
                    return render_template('add.html', error=error, all_data=all_data, username=username)

            # Register user
            if request.form['submit'] == 'REGISTER':
                rank = request.form['rank']
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                new_username = request.form['new_username']
                new_password = request.form['new_password']
                if firstname == "" or lastname == "" or new_username == "" or new_password == "":
                    error = "one of the fields are empty"
                    return render_template('add.html', error=error, all_data=all_data, username=username)
                else:
                    error = User_LRCHR.user_check(rank, firstname, lastname, new_username, new_password, users, conn)
                    return render_template('add.html', error=error, all_data=all_data, username=username)

        else:
            if "username" in session:
                username = session["username"]
                username_ch = session["username"]
                # check username rank for access this page
                if User_LRCHR.check_rank(username_ch, users) == True:
                    return render_template('add.html', username=username, all_data=all_data)
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
    all_data[0] = sort_data_by_name.sort_data(all_data)
    ping_data.clear()
    # currency()