from datetime import datetime
from scripts import sql_job

# log
def in_to_the_log(event):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    sql_job.insert_to_log_sql(dt_string, event)
    sql_job.import_logs()