# -*- coding: latin-1 -*-
import psutil

import subprocess
from os import path
from time import sleep
from ..helpers import csv_to_dict
from ..constants import dirname

def get_battery_info():
    program = path.join(dirname, 'programs/battery_info.exe')
    subprocess.run([program, '/scomma', 'battery.csv'], shell=True)

    filename = "./battery.csv"
    result_dict = csv_to_dict(filename)
    
    return [result_dict]


# todo get health info

def is_battery_installed():
    return psutil.sensors_battery() != None


__all__ = ['battery']