from scripts import sql_job

#register
def register(rank, firstname, lastname, new_username, new_password, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    cursor.execute(f" insert into users(rank, username, password, firstname, lastname) values ('{str(rank)}', '{str(new_username)}', '{str(new_password)}', '{str(firstname)}', '{str(lastname)}')")
    conn.commit()
    sql_job.import_users()

# check username exist before register
def user_check(rank, firstname, lastname, new_username, new_password, users, conn):
    if new_username in users:
        error = f"{new_username} is allready exist"
        return error
    else:
        register(rank, firstname, lastname, new_username, new_password, conn)
        error = "user registered successfully"
        return error

# check rank for user
def check_rank(username_ch, users):
    if username_ch in users:
        user = users[username_ch]
        if not "3" == user['rank']:
            return False
        else:
            return True

# user login
def user_login(users, username, password):
    if username not in users:
        return False
    else:
        user = users[username]
        if not password == user["password"]:
            return False
        else:
            return True