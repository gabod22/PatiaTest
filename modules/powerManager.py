import os

from .constants import power_scheme_path
from .helpers.system_accions import run_powershell_command


def set_configuration_to_current_scheme():
    os.popen('powercfg /change monitor-timeout-ac 0')
    os.popen('powercfg /change monitor-timeout-dc 0')
    os.popen('powercfg /change standby-timeout-ac 0')
    os.popen('powercfg /change standby-timeout-dc 0')


def set_default_configuration():
    os.popen('powercfg /change monitor-timeout-ac 10')
    os.popen('powercfg /change monitor-timeout-dc 5')
    os.popen('powercfg /change standby-timeout-ac 30')
    os.popen('powercfg /change standby-timeout-dc 15')
    
def set_showroom_configuration():
    os.popen('powercfg /change monitor-timeout-ac 0')
    os.popen('powercfg /change monitor-timeout-dc 5')
    os.popen('powercfg /change standby-timeout-ac 0')
    os.popen('powercfg /change standby-timeout-dc 10')


def set_brightness(level):
    run_powershell_command(
        "powershell -Command (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,"+level+")")


def get_default_power_scheme():
    commnad = "POWERCFG /GETACTIVESCHEME"
    return os.popen(commnad).read()[25:62]


def get_saved_default_power_scheme(file_path):
    text_file = open(file_path, "r")
    return text_file.read()
