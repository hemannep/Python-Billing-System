def display_equipment(equipment_list):
    max_name_length = max(len(equipment['name']) for equipment in equipment_list)
    max_brand_length = max(len(equipment['brand']) for equipment in equipment_list)
    max_quantity_length = len(str(max(equipment['quantity'] for equipment in equipment_list)))

    print("╔════════════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║ {'SN.':<8} {'Equipment Name':<{max_name_length + 2}} {'Brand':<{max_brand_length + 2}} {'Price (5 days)':<15} {'Quantity':<{max_quantity_length}}      ║")
    print("╟────────────────────────────────────────────────────────────────────────────────────────╢")
    
    for i, equipment in enumerate(equipment_list, start=1):
        print(f"║ {i:<8} {equipment['name']:<{max_name_length + 2}} {equipment['brand']:<{max_brand_length + 2}} ${equipment['price']:<15.2f} {equipment['quantity']:<{max_quantity_length}}         ║")
    
    print("╚════════════════════════════════════════════════════════════════════════════════════════╝")
    