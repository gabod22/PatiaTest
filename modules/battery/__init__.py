# -*- coding: latin-1 -*-
import psutil
import csv
import subprocess
from os import path
from ..constants import dirname


def get_battery_info():
    program = path.join(dirname, "programs/battery_info.exe")
    subprocess.run([program, "/scomma", path.join(dirname, "battery.csv")], shell=True)
    result_list = []
    data = []

    filename = path.join(dirname, "battery.csv")
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            data.append(row)

    for battery in range(1, len(header)):
        battery_dict = {}
        for row in data:
            key = row[0]
            values = row[battery]
            battery_dict[key] = values
        result_list.append(battery_dict)
        # print('Termine el ', battery)
    return result_list


# def wmi_get_battery_info():
#     w = wmi.WMI()
#     for battery in w.query('select * from Win32_Battery'):
#         print battery.EstimatedChargeRemaining


# todo get health info


def is_battery_installed():
    return psutil.sensors_battery() != None


# __all__ = ['battery']
