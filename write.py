def write_equipment_file(file_name, equipment_list):
    with open(file_name, 'w') as file:
        for equipment in equipment_list:
            line = f"{equipment['name']}, {equipment['brand']}, ${equipment['price']:.2f}, {equipment['quantity']}\n"
            file.write(line)
            