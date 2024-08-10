import datetime
import math
from read import read_equipment_file
from display import display_equipment
from operation import find_equipment_by_serial_number, calculate_charged_duration
from write import write_equipment_file


def rent_equipment(equipment_list, customer_name):
    while True:
        try:
            total_quantity = int(input("Enter the total number of items you want to rent: "))
            if total_quantity <= 0:
                print("Invalid quantity! Please enter a valid quantity.")
                continue

            rented_items = []
            for _ in range(total_quantity):
                while True:
                    serial_number = int(input("Enter the serial number of the equipment to rent: "))
                    equipment = find_equipment_by_serial_number(equipment_list, serial_number)

                    if equipment is None:
                        print("Invalid serial number! Please enter a valid serial number.")
                        continue
                    
                    print(f"Selected equipment: {equipment['name']}")
                    break

                while True:
                    quantity = int(input(f"Enter the quantity of '{equipment['name']}' you want to rent: "))
                    if quantity <= 0 or quantity > equipment['quantity']:
                        print("Invalid quantity! Please enter a valid quantity.")
                        continue
                    break

                rented_items.append({'equipment': equipment, 'quantity': quantity})

            while True:
                total_days = int(input("Enter the number of days you want to rent the equipment: "))
                if total_days <= 0:
                    print("Invalid number of days! Please enter a valid value.")
                    continue
                break

            while True:
                customer_contact = input("Enter your contact number (10 digits): ")
                if len(customer_contact) == 10 and customer_contact.isdigit():
                    break
                else:
                    print("Invalid contact number! Please enter a 10-digit number.")

            customer_address = input("Enter your address: ")

            total_amount = sum(item['equipment']['price'] * total_days / 5 * item['quantity'] for item in rented_items)
            rental_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            invoice_data = {
                "Customer": customer_name,
                "Contact Number": customer_contact,
                "Address": customer_address,
                "Items Rented": []
            }

            for item in rented_items:
                equipment = item['equipment']
                quantity = item['quantity']
                item_data = {
                    "Equipment": equipment['name'],
                    "Brand": equipment['brand'],
                    "Rental Date": rental_date,
                    "Actual Rental Duration": f"{total_days} days",
                    "Total Amount": f"${equipment['price'] * total_days / 5 * quantity:.2f}"
                }
                invoice_data["Items Rented"].append(item_data)

                equipment['quantity'] -= quantity
                write_equipment_file("equipment.txt", equipment_list)

            invoice_file_name = f"{customer_name.replace(' ', '_')}_rental_invoice.txt"
            with open(invoice_file_name, 'w') as file:
                file.write("-------------- Rental Invoice --------------\n")
                for key, value in invoice_data.items():
                    if key == "Items Rented":
                        for item in value:
                            file.write("\n".join([f"{item_key}: {item_value}" for item_key, item_value in item.items()]) + "\n\n")
                    else:
                        file.write(f"{key}: {value}\n")

            print("Equipment rented successfully!")
            display_invoice(invoice_data)

            another_item = input("Do you want to add another item? (Y/N): ")
            if another_item.lower() != 'y':
                break

        except ValueError:
            print("Invalid input! Please enter valid values.")

def return_equipment(equipment_list, customer_name):
    while True:
        try:
            total_quantity = int(input("Enter the total number of items you want to return: "))
            if total_quantity <= 0:
                print("Invalid quantity! Please enter a valid quantity.")
                continue

            returned_items = []
            for _ in range(total_quantity):
                while True:
                    serial_number = int(input("Enter the serial number of the equipment to return: "))
                    equipment = find_equipment_by_serial_number(equipment_list, serial_number)
                    
                    if equipment is None:
                        print("Invalid serial number! Please enter a valid serial number.")
                        continue

                    print(f"Selected equipment: {equipment['name']}")
                    break

                while True:
                    quantity = int(input(f"Enter the quantity of '{equipment['name']}' you want to return: "))
                    if quantity <= 0:
                        print("Invalid quantity! Please enter a valid quantity.")
                        continue
                    break

                returned_items.append({'equipment': equipment, 'quantity': quantity})

            while True:
                total_days = int(input("Enter the number of days you rented the equipment: "))
                if total_days <= 0:
                    print("Invalid number of days! Please enter a valid value.")
                    continue
                break

            while True:
                customer_contact = input("Enter your contact number (10 digits): ")
                if len(customer_contact) == 10 and customer_contact.isdigit():
                    break
                else:
                    print("Invalid contact number! Please enter a 10-digit number.")

            customer_address = input("Enter your address: ")

            total_amount = sum(item['equipment']['price'] * total_days / 5 * item['quantity'] for item in returned_items)
            rental_date_str = (datetime.datetime.now() - datetime.timedelta(days=total_days)).strftime("%Y-%m-%d")
            rental_date = datetime.datetime.strptime(rental_date_str, "%Y-%m-%d")
            invoice_data = {
                "Customer": customer_name,
                "Contact Number": customer_contact,
                "Address": customer_address,
                "Items Returned": []
            }

            for item in returned_items:
                equipment = item['equipment']
                quantity = item['quantity']
                rental_date_item = rental_date.strftime("%Y-%m-%d %H:%M:%S")
                item_data = {
                    "Equipment": equipment['name'],
                    "Brand": equipment['brand'],
                    "Rental Date for Item": rental_date_item,
                    "Actual Rental Duration for Item": f"{total_days} days",
                    "Total Amount for Item": f"${equipment['price'] * total_days / 5 * quantity:.2f}"
                }
                invoice_data["Items Returned"].append(item_data)

                equipment['quantity'] += quantity
                write_equipment_file("equipment.txt", equipment_list)

            invoice_file_name = f"{customer_name.replace(' ', '_')}_return_invoice.txt"
            with open(invoice_file_name, 'w') as file:
                file.write("-------------- Return Invoice --------------\n")
                for key, value in invoice_data.items():
                    if key == "Items Returned":
                        for item in value:
                            file.write("\n".join([f"{item_key}: {item_value}" for item_key, item_value in item.items()]) + "\n\n")
                    else:
                        file.write(f"{key}: {value}\n")

            print("Equipment returned successfully!")
            display_invoice(invoice_data)

            another_item = input("Do you want to return another item? (Y/N): ")
            if another_item.lower() != 'y':
                break

        except ValueError:
            print("Invalid input! Please enter valid values.")


def display_invoice(invoice_data):
    print("╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                        ------ Invoice ------                                              ║")
    print("╟───────────────────────────────────────────────────────────────────────────────────────────────────────────╢")
    
    for key, value in invoice_data.items():
        if key == "Items Rented" or key == "Items Returned":
            print(f"║ {key}:")
            for item in value:
                print("║   " + "\n║   ".join([f"{item_key}: {item_value}" for item_key, item_value in item.items()]))
        else:
            print(f"║  {key:<59}\t{value:<32}            ")
            
    print("╚═══════════════════════════════════════════════════════════════════════════════════════════════════════════╝")




def main_menu():
    equipment_file_name = "equipment.txt"
    equipment_list = read_equipment_file(equipment_file_name)

    while True:
        print()  # New line for better readability

        print("\n╔══════════════════════════════════════════════════════════════════════════════════════╗")
        print("╟───────────|                   Welcome To BH Rental House                 |───────────╢")
        print("╚══════════════════════════════════════════════════════════════════════════════════════╝")

        print("\n╔═══════════════════════╗")
        print("║  Select an action:    ║")
        print("╟───────────────────────╢")
        print("║  1. Display items     ║")
        print("║  2. Rent Equipment    ║")
        print("║  3. Return Equipment  ║")
        print("║  4. Quit              ║")
        print("╚═══════════════════════╝")
        choice = input("Enter your choice (1-4): ")

        if choice.lower() == '1':
            display_equipment(equipment_list)

            while True:
                print("\n╔═══════════════════════╗")
                print("║  Select an action:    ║")
                print("╟───────────────────────╢")
                print("║  a. Rent Equipment    ║")
                print("║  b. Return Equipment  ║")
                print("║  c. Quit              ║")
                print("╚═══════════════════════╝")
                new_choice = input("Enter your choice (a-c): ")

                if new_choice.lower() == 'a':
                    customer_name = input("Enter your name: ")
                    rent_equipment(equipment_list, customer_name)
                    break
                elif new_choice.lower() == 'b':
                    customer_name = input("Enter your name: ")
                    return_equipment(equipment_list, customer_name)
                    break
                elif new_choice.lower() == 'c':
                    print('Hope you will rent goods from us next time!!')
                    print("                Thank You!!                 ")
                    break
                else:
                    print("Invalid choice! Please choose a value between a-c.")

        elif choice.lower() == '2':
            customer_name = input("Enter your name: ")
            rent_equipment(equipment_list, customer_name)
        elif choice.lower() == '3':
            customer_name = input("Enter your name: ")
            return_equipment(equipment_list, customer_name)
        elif choice.lower() == '4':
            print('Hope you will rent goods from us next time!!')
            print("                Thank You!!                 ")
            break
        else:
            print("Invalid choice! Please choose a value between 1 and 4.")

if __name__ == '__main__':
    main_menu()