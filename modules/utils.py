# -*- coding: latin-1 -*-
import math

import socket
import ctypes
import psutil
def p2f(x: str):
    return float(x.strip("%")) / 100


def wmiToDict(wmi_object):
    return dict(
        (attr, getattr(wmi_object, attr)) for attr in wmi_object.__dict__["_properties"]
    )


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

#comprobacion de adminsitrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Comprobaciones de red
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



def is_battery_installed():
    return psutil.sensors_battery() != None