import datetime
import math
from read import read_equipment_file

def find_equipment_by_serial_number(equipment_list, serial_number):
    if serial_number >= 1 and serial_number <= len(equipment_list):
        return equipment_list[serial_number - 1]
    return None

def calculate_charged_duration(total_days):
    charged_duration = math.ceil(total_days / 5) * 5
    return charged_duration
