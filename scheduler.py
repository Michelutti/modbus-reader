import schedule
import time


def job():
    read_modbus_and_save()


schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
