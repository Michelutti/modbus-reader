from pyModbusTCP.client import ModbusClient
from time import sleep
c = ModbusClient(host="192.168.15.75", port=502, unit_id=1, auto_open=True)
while True:
    regs = c.read_discrete_inputs(0,8)
    if regs:
        print(regs)
    else:
        print("read error")
    regs = c.read_input_registers(0,6)
    if regs:
        print(regs)
    else:
        print("read error")
    regs = c.read_holding_registers(0,6)
    if regs:
        print(regs)
    else:
        print("read error")
    sleep(1)