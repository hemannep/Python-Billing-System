def read_equipment_file(file_name):
    equipment_list = []
    with open(file_name, 'r') as file:
        for line in file:
            data = line.strip().split(', ')
            name = data[0]
            brand = data[1]
            price = float(data[2].replace('$', ''))
            quantity = int(data[3])
            equipment_list.append({'name': name, 'brand': brand, 'price': price, 'quantity': quantity})
    return equipment_list
