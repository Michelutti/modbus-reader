import certifi
ca = certifi.where()
import time
from pymongo import MongoClient
from pyModbusTCP.client import ModbusClient

import json

# Replace 'your_file.json' with the actual path to your JSON file
file_path = 'settings.json'
settings_data = ''

try:
    with open(file_path, 'r') as json_file:
        settings_data = json.load(json_file)
        # Now 'data' contains the contents of the JSON file as a Python data structure
        print(settings_data)
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
    discreteInputs = client.read_discrete_inputs(0, 6)
    inputRegister = client.read_input_registers(0, 6)
    print(discreteInputs)
    print(inputRegister)
    # result = [{'input': boolean, 'value': integer} for boolean, integer in zip(discreteInputs, inputRegister)]
  
    # if result:
    #     print(result)
    # else:
    #     print("read error")
    #     return None

    return generate_results(settings_data, inputRegister, discreteInputs)

def store_data_in_mongodb(data):
    if data:
        collection.insert_many(data)

def generate_results(data, inputRegister, discreteInput):
    results = []
    timestamp = time.time()

    while inputRegister and discreteInput:
        machine_added = False

        for item in data:
            machine = item['machine']
            map_data = item['map']

            if len(inputRegister) >= machine['inputRegister'] and len(discreteInput) >= machine['discreteInput']:
                result_object = {
                    'machine': len(results) +1,
                    'timestamp': timestamp
                }

                for mapping in map_data:
                    data_type = mapping['tipo']
                    address = mapping['endereco']

                    if data_type == 'discreteInput':
                        result_object[mapping['descricao']] = discreteInput.pop(0)
                    elif data_type == 'inputRegister':
                        result_object[mapping['descricao']] = inputRegister.pop(0)

                results.append(result_object)
                machine_added = True

        if not machine_added:
            # If no machine was added in this iteration, exit the loop
            break

    return results

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