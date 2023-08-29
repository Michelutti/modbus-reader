import sqlite3
import schedule


def save_to_sqlite():
    conn = sqlite3.connect('modbus_data.db')
    cursor = conn.cursor()

    with open('modbus_data.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split(',')
            cursor.execute('INSERT INTO modbus_data VALUES (?, ?, ?)', data)  # Modify the query

    conn.commit()
    conn.close()


schedule.every(15).minutes.do(save_to_sqlite)

while True:
    schedule.run_pending()
    time.sleep(1)
