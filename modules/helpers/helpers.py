# -*- coding: latin-1 -*-
from PySide6.QtWidgets import QTableWidgetItem
import wave



def add_data_to_table(array: list, table):
    for row in range(len(array)):
        for column in range(len(array[row])):
            table.setItem(row, column, QTableWidgetItem(str(array[row][column])))


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



def calculate_wav_duration(path):

    with wave.open(path) as mywav:
        duration_seconds = mywav.getnframes() / mywav.getframerate()
        print(f"Length of the WAV file: {duration_seconds:.1f} s")

    return duration_seconds

def filter_exe_files(file):
    if file.find('.exe') > 0:
        return True
    return False

