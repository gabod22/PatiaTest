# -*- coding: latin-1 -*-

import os

import sys
import winsound
import wmi
import GPUtil


from modules.helpers import *
from multiprocessing import freeze_support

dirname = os.path.dirname(__file__)

c = wmi.WMI()
t = wmi.WMI(moniker="//./root/wmi")
bios = c.Win32_BIOS()[0]

my_system = c.Win32_ComputerSystem()[0]
freeze_support()
#cpu_info = get_cpu_info()

def sync_date_time():
    run_powershell_command('net stop w32time')
    run_powershell_command('w32tm /unregister')
    run_powershell_command('w32tm /register')
    run_powershell_command('net start w32time')
    run_powershell_command('w32tm /resync')



def get_gpu_percent():
    gpus = GPUtil.getGPUs()
    if len(gpus) > 0:
        return gpus[0].load
    return 0


#Get Disks information
def get_disks_info():
    disks = []
    for drive in c.query("SELECT * FROM Win32_DiskDrive"):
        if(drive.InterfaceType != 'USB'):
            disks.append(
            [drive.Caption, drive.InterfaceType, convert_size(int(drive.Size)), drive.Status]
            )
    return disks

def get_disks():
    text = ""
    for drive in c.query("SELECT * FROM Win32_DiskDrive"):
        if(drive.InterfaceType != 'USB'):
            text = text + 'm: %s, t: %s, i: %s, s: %s;' % (drive.Caption, convert_size(int(drive.Size)), drive.InterfaceType, drive.Status)
    return text



#Sound tests
def play_speaker_test_sound():
    soundtest = os.path.join(dirname, 'assets\soundtest.wav')
    winsound.PlaySound(soundtest, winsound.SND_ASYNC)

def stop_speaker_test_sound():
    winsound.PlaySound(None, winsound.SND_PURGE)