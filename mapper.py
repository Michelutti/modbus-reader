def generate_results(data, inputRegister, discreteInput):
    results = []

    while inputRegister and discreteInput:
        machine_added = False

        for item in data:
            machine = item['machine']
            map_data = item['map']

            if len(inputRegister) >= machine['inputRegister'] and len(discreteInput) >= machine['discreteInput']:
                result_object = {
                    'machine': len(results) +1,
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

data = [
    {
        "tipo": "LigaDesliga",
        "machine": {
            "inputRegister": 2,
            "discreteInput": 1
        },
        "map": [
            {
                "tipo": "discreteInput",
                "endereco": 1,
                "descricao": "liga_desliga"
            },
            {
                "tipo": "inputRegister",
                "endereco": 1,
                "descricao": "velocidade"
            },
            {
                "tipo": "inputRegister",
                "endereco": 2,
                "descricao": "temperatura"
            }
        ]
    }
]

inputRegister = ["1a", "2b", "3c", "4d", "5e", "6f", "7g", "8h", "9i", "10j"]
discreteInput = [1, 2, 3, 4, 5]

results = generate_results(data, inputRegister, discreteInput)
print(results)
