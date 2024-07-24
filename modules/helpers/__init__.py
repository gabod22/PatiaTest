# -*- coding: latin-1 -*-
import math
import os
import subprocess
import socket
from ..constants import dirname
import ctypes
from PySide6.QtWidgets import QTableWidgetItem
import wave
from pathlib import Path


def add_data_to_table(array: list, table):
    for row in range(len(array)):
        for column in range(len(array[row])):
            table.setItem(row, column, QTableWidgetItem(str(array[row][column])))


def p2f(x: str):
    return float(x.strip("%")) / 100


def wmiToDict(wmi_object):
    return dict(
        (attr, getattr(wmi_object, attr)) for attr in wmi_object.__dict__["_properties"]
    )


def open_program(program_path):
    """Ejecuta un programa dentro especificado

    Args:
        program (str): Ubicación absoluta del programa
    """
    
    try:
        path = Path(program_path)
        filename = path.name
        print("Abriendo el programa {0} ".format(filename))
        os.popen(program_path)

    except Exception as e:
        print("No se pudo ejectutar el programa {0} por un error: {1}".format(program_path, e))


def run_powershell_command(command):
    """Esta funcion ejecuta un comando con powershell

    Args:
        command (str): Es el comando que se va a ejecutar de powershell
    """
    subprocess.run(command, shell=True)


def kill_process_by_name(name):
    subprocess.run("taskkill /IM " + name + " /F")


def toPercent(ratio):
    return str(round(ratio * 100, 2)) + "%"


def txt_to_lst(file_path):
    try:
        stopword = open(file_path, "r")
        return stopword.read().split("\n")
    except Exception as e:
        print(e)


def convert_size(size_bytes):
    size_bytes = int(size_bytes)

    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 0)
    return "%s %s" % (s, size_name[i])


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)


# def add_new_row(worksheet):
#     return worksheet.row_count

# def next_available_row(worksheet):
#     worksheet.row_count
#     str_list = list(filter(None, worksheet.col_values(1)))
#     return str(len(str_list)+1)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def isConnected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            print("Clossing socket")
            sock.close
        return True
    except OSError:
        pass
    return False


def WMIDateStringToDate(dtmDate):
    strDateTime = ""
    if dtmDate[4] == 0:
        strDateTime = dtmDate[5] + "/"
    else:
        strDateTime = dtmDate[4] + dtmDate[5] + "/"
    if dtmDate[6] == 0:
        strDateTime = strDateTime + dtmDate[7] + "/"
    else:
        strDateTime = strDateTime + dtmDate[6] + dtmDate[7] + "/"
        strDateTime = (
            strDateTime
            + dtmDate[0]
            + dtmDate[1]
            + dtmDate[2]
            + dtmDate[3]
            + " "
            + dtmDate[8]
            + dtmDate[9]
            + ":"
            + dtmDate[10]
            + dtmDate[11]
            + ":"
            + dtmDate[12]
            + dtmDate[13]
        )
    return strDateTime


def get_registry_value(key, subkey, value):
    import winreg

    key = getattr(winreg, key)
    handle = winreg.OpenKey(key, subkey)
    (value, type) = winreg.QueryValueEx(handle, value)
    return value


def calculate_wav_duration(path):

    with wave.open(path) as mywav:
        duration_seconds = mywav.getnframes() / mywav.getframerate()
        print(f"Length of the WAV file: {duration_seconds:.1f} s")

    return duration_seconds
