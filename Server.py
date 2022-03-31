from multiprocessing.dummy import Pool as ThreadPool
from turtle import update
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from pythonping import ping
import time, threading
from waitress import serve
from scripts import ip_check, RPR, User_LRCHR, panel, sort_data_by_name, sql_job, get_ip_server, updates

pool = ThreadPool(3)
ping_data = []
time_refresh = 10
data = []
username = ""
all_devices = 0
currency_number = []

print(get_ip_server.get_ip())
all_data, users = sql_job.return_import()

# Ping Calc
def ping_system(ip):
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
            move_save = []
            move_save = request.get_json()
            # sql_job.save_move_position(data)
            print(move_save)
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

    # Log
    @app.route("/log", methods=['POST', 'GET'])
    def log():
        if "username" in session:
            username = session["username"]
            return render_template('log.html', username=username, all_data=all_data[1])
        else:
            return redirect(url_for('login'))

    # Add
    @app.route("/add", methods=['POST', 'GET'])
    def add():
        error = None
        global username
        models_list = list(all_data[3][0])
        # Add tower
        if request.method == 'POST':
            if request.form['submit'] == 'Add Tower':
                tower_name = request.form['tower_name']
                address = request.form['tower_name']
                if tower_name == "":
                    error = 'Empty - Choose a name for your tower'
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                else:
                    error = panel.check_tower_name(all_data, tower_name, address)
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)

            # Add device
            if request.form['submit'] == 'ADD DEVICE':
                radio_name = request.form['radio_name']
                radio_ip = request.form['radio_ip']
                to_tower = request.form['tower_name']
                mode = request.form['mode']
                model = request.form['models']
                if "" in (radio_name, radio_ip, to_tower, mode, model):
                    error = 'One of these fields are empty'
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                else:
                    if ip_check.ip_format_check(radio_ip) == True:
                        panel.add_radio(radio_name, radio_ip, to_tower, mode, model, all_data)
                        error = f'{radio_name} in tower {to_tower} with ip {radio_ip} added successfully'
                        return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                    else:
                        error = f'ip {radio_ip} is incorect'
                        return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)

            # delete tower name
            if request.form['submit'] == 'Delete Tower':
                delete_tower_name = ""
                delete_tower_name = request.form['delete']
                if "None" in delete_tower_name:
                    error = "Choose a tower"
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                else:
                    error = f"{delete_tower_name} Successfully deleted"
                    panel.delete_tower(delete_tower_name, all_data)
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)

            # Edit tower name
            if request.form['submit'] == 'Change tower name':
                target_tower_name = request.form['target_tower_name']
                new_tower_name = request.form['new_tower_name']
                if new_tower_name == "":
                    error = "Choose a new name for your tower"
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                else:
                    i = 0
                    while len(all_data[2]) > i:
                        if all_data[2][i]['tower_name'] == new_tower_name:
                            error = f'{new_tower_name} is all ready exist'
                            return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                        else:
                            i = i + 1
                    if i == len(all_data[2]):
                        error = f"Successfully changed from {target_tower_name} to {new_tower_name}"
                        panel.edit_tower_name(new_tower_name, target_tower_name)
                        return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)

            # Edit device name
            if request.form['submit'] == 'Change radio name':
                target_radio_name = request.form['target_radio_name']
                new_radio_name = request.form['new_radio_name']
                if new_radio_name == "":
                    error = "Choose a new name for your radio"
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                else:
                    i = 0
                    while len(all_data[0]) > i:
                        if all_data[0][i]['ap_name'] == new_radio_name:
                            error = f'{new_radio_name} is all ready exist'
                            return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                        else:
                            i = i + 1
                    if i == len(all_data[0]):
                        error = f"Successfully changed from {target_radio_name} to {new_radio_name}"
                        panel.edit_radio_name(new_radio_name, target_radio_name, all_data)
                        return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)

            # Add model
            if request.form['submit'] == 'add device model':
                device_model = request.form['device_model']
                device_os = request.form['device_os']
                if device_model == "":
                    error = "Type a device name"
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                else:
                    error = "done"
                    panel.add_model(device_model, device_os, all_data)
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)

            # delete device name
            if request.form['submit'] == 'Delete device name':
                delete_device_name = ""
                delete_device_name = request.form['target_device_name']
                if "None" in delete_device_name:
                    error = "Choose a tower"
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                else:
                    error = f"{delete_device_name} Successfully deleted"
                    panel.delete_device(delete_device_name, all_data)
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)

            # Register user
            if request.form['submit'] == 'REGISTER':
                rank = request.form['rank']
                firstname = request.form['firstname']
                lastname = request.form['lastname']
                new_username = request.form['new_username']
                new_password = request.form['new_password']
                if firstname == "" or lastname == "" or new_username == "" or new_password == "":
                    error = "one of the fields are empty"
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list)
                else:
                    error = User_LRCHR.user_check(rank, firstname, lastname, new_username, new_password, users, models_list=models_list )
                    return render_template('add.html', error=error, all_data=all_data, username=username, models_list=models_list )

        else:
            if "username" in session:
                username = session["username"]
                username_ch = session["username"]
                # check username rank for access this page
                if User_LRCHR.check_rank(username_ch, users) == True:
                    return render_template('add.html', username=username, all_data=all_data, models_list=models_list )
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
    all_data[0] = RPR.replace(ping_data, all_data)
    all_data[0] = sort_data_by_name.sort_data(all_data)
    ping_data.clear()
    # currency()