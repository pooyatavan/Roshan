from scripts import import_from_sql

#register
def register(rank, firstname, lastname, new_username, new_password, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    cursor.execute(f" insert into users(rank, username, password, firstname, lastname) values ('{str(rank)}', '{str(new_username)}', '{str(new_password)}', '{str(firstname)}', '{str(lastname)}')")
    conn.commit()

# check username exist before register
def user_check(rank, firstname, lastname, new_username, new_password, all_data, conn):
    counter = 0
    while True:
        if len(all_data[1]) == counter:
            register(rank, firstname, lastname, new_username, new_password, conn)
            error = "user registered successfully"
            refresh_users_list = import_from_sql.import_users()
            return error, refresh_users_list
        else:
            if new_username == all_data[1][counter]['username'] == new_username:
                error = f"{new_username} is allready exist"
                return error
            else:
                counter = counter + 1

# check rank for user
def check_rank(username, all_data):
    user_check_counter = 0
    while True:
        if len(all_data[1]) >= user_check_counter:
            if all_data[1][user_check_counter]['username'] == username:
                if all_data[1][user_check_counter]['rank'] == "3":
                    return True
                else:
                    return False
            else:
                user_check_counter = user_check_counter + 1
        else:
            break

# user login
def user_login(all_data, username, password):
    user_check_counter = 0
    while True:
        if len(all_data[1]) > user_check_counter:
            if all_data[1][user_check_counter]['username'] == username:
                if all_data[1][user_check_counter]['password'] == password:
                    return True
                break
            else:
                user_check_counter = user_check_counter + 1
        else:
            return False
