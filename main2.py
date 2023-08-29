import time
from pymongo import MongoClient
from pyModbusTCP.client import ModbusClient

# Modbus Configuration
modbus_ip = "192.168.15.75"
modbus_port =  502 # Default Modbus TCP port
modbus_slave_address = 1  # Change to your Modbus slave address

# MongoDB Configuration
mongo_client = MongoClient('mongodb://localhost:27017/')  # Change if MongoDB is running on a different host or port
db = mongo_client['modbus_data']
collection = db['readings']

client = ModbusClient(host="192.168.15.75", port=502, unit_id=1, auto_open=True)

def read_modbus_data():
    discreteInputs = client.read_discrete_inputs(0, 1)
    inputRegister = client.read_input_registers(0, 1)

    result = [{'input': boolean, 'value': integer} for boolean, integer in zip(discreteInputs, inputRegister)]

    if result:
        print(result)
    else:
        print("read error")
        return None
    return result

def store_data_in_mongodb(data):
    if data:
        collection.insert_one({'data': data, 'timestamp': time.time()})

while True:
    # Read Modbus data and store it in MongoDB
    modbus_data = read_modbus_data()
    # store_data_in_mongodb(modbus_data)

    # Wait for 30 seconds
    time.sleep(1)

    # Check if 15 minutes have passed and perform MongoDB cleanup
    current_time = time.time()
    #if current_time % (15 * 60) < 30:
        # Remove old data (optional)
        #collection.delete_many({'timestamp': {'$lt': current_time - (15 * 60)}})
