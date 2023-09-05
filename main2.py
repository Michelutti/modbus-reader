import certifi
ca = certifi.where()
import time
from pymongo import MongoClient
from pyModbusTCP.client import ModbusClient

import json

# Replace 'your_file.json' with the actual path to your JSON file
file_path = 'settings.json'

try:
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        # Now 'data' contains the contents of the JSON file as a Python data structure
        print(data)
except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")

# Modbus Configuration
modbus_ip = "192.168.15.75"
modbus_port =  502 # Default Modbus TCP port
modbus_slave_address = 1  # Change to your Modbus slave address

# MongoDB Configuration
mongo_client = MongoClient('', tlsCAFile=ca)  # Change if MongoDB is running on a different host or port
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
    store_data_in_mongodb(modbus_data)

    # Wait for 30 seconds
    time.sleep(5)

    # Check if 15 minutes have passed and perform MongoDB cleanup
    # current_time = time.time()
    #if current_time % (15 * 60) < 30:
        # Remove old data (optional)
        #collection.delete_many({'timestamp': {'$lt': current_time - (15 * 60)}})


# collection.insert_one({'data': 1, 'timestamp': time.time()})