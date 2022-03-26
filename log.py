from datetime import datetime
from scripts import import_from_sql

# log
def in_to_the_log(conn, event):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    cursor = conn.cursor() 
    cursor.execute('SELECT * FROM log')
    cursor.execute(f" insert into log(date, event) values ('{dt_string}', '{str(event)}')")
    conn.commit()
    import_from_sql.import_logs()