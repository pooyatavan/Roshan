from scripts import log, sql_job

# Create tower
def create_tower(all_data, tower_name, address):
    if check_tower_name(all_data, tower_name) == True:
        return f'{tower_name} is all ready exist'
    else:
        sql_job.insert_tower_name(tower_name, address)
        sql_job.sort_id_for_tower()
        event = f"Tower {tower_name} was added"
        log.in_to_the_log(event)
        return f'{tower_name} added successfully'

# check tower name if allready exist
def check_tower_name(all_data, tower_name):
    i = 0
    while len(all_data[2]) > i:
        if all_data[2][i]['tower_name'] == tower_name:
            return True
        else:
            i = i + 1
    if i == len(all_data[2]):
        return False

# Delete tower
def delete_tower(delete_tower_name):
    sql_job.delete_tower_from_sql(delete_tower_name)
    sql_job.sort_id_for_tower()
    event = f"Tower {delete_tower_name} deleted"
    log.in_to_the_log(event)

# Edit tower name
def edit_tower_name(new_tower_name, target_tower_name, all_data):
    if check_tower_name(all_data, new_tower_name) == True:
        return f'{new_tower_name} is all ready exist'
    else:
        event = f"Tower name from {target_tower_name} to {new_tower_name} has changed"
        log.in_to_the_log(event)
        sql_job.edit_tower_name(new_tower_name, target_tower_name)
        sql_job.sort_id_for_tower()
        return f"Tower name from {target_tower_name} to {new_tower_name} has changed"

########################################################

# Delete device
def delete_device(delete_device_name, all_data):
    sql_job.delete_device_sql(delete_device_name, all_data)
    event = f"Device {delete_device_name} was deleted"
    log.in_to_the_log(event)

# Add radio
def add_radio(radio_name, radio_ip, to_tower, mode, model, all_data):
    os = all_data[3][0].get(f"{model}")
    sql_job.insert_device(radio_name, radio_ip, to_tower, mode, model, os, all_data)
    event = f"Device {radio_name} added"
    log.in_to_the_log(event)

# Edit radio name
def edit_radio_name(new_radio_name, target_radio_name, all_data):
    i = 0
    while len(all_data[0]) > i:
        if all_data[0][i]['device_name'] == new_radio_name:
            return f'{new_radio_name} is all ready exist'
        else:
            i = i + 1
    if i == len(all_data[0]):
        sql_job.edit_device_name_sql(all_data, target_radio_name)
        event = f"Radio name changed from {target_radio_name} to {new_radio_name}"
        log.in_to_the_log(event)
        return f'{target_radio_name} renamed successfully to {new_radio_name}'

########################################################

# Add model
def add_model(device_model, device_os, all_data):
    sql_job.insert_model_sql(device_model, device_os)
    all_data[3] = []
    event = f"Device model {device_model} added"
    log.in_to_the_log(event)