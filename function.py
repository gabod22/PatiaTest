# -*- coding: latin-1 -*-

import os

import winsound
import wmi
import wave
from time import sleep

# import GPUtil


from modules.helpers import *
from multiprocessing import freeze_support
from modules.constants import dirname

c = wmi.WMI()
t = wmi.WMI(moniker="//./root/wmi")
bios = c.Win32_BIOS()[0]

my_system = c.Win32_ComputerSystem()[0]
freeze_support()
# cpu_info = get_cpu_info()

def calculate_wav_duration(path):
    
    with wave.open(path) as mywav:
        duration_seconds = mywav.getnframes() / mywav.getframerate()
        print(f"Length of the WAV file: {duration_seconds:.1f} s")
        
    return duration_seconds


def sync_date_time():
    run_powershell_command("net stop w32time")
    run_powershell_command("w32tm /unregister")
    run_powershell_command("w32tm /register")
    run_powershell_command("net start w32time")
    run_powershell_command("w32tm /resync")


# def get_gpu_percent():
#     gpus = GPUtil.getGPUs()
#     if len(gpus) > 0:
#         return gpus[0].load
#     return 0


# Sound tests
def play_speaker_test_sound():
    soundtest = os.path.join(dirname, "assets/soundtest.wav")
    
    winsound.PlaySound(soundtest, winsound.SND_ASYNC)
    


def stop_speaker_test_sound():
    winsound.PlaySound(None, winsound.SND_PURGE)


def play_cansado_sound():
    soundtest = os.path.join(dirname, "assets/estoy-cansado-jefe.wav")
    duration = calculate_wav_duration(soundtest)
    winsound.PlaySound(soundtest, winsound.SND_ASYNC)
    sleep(duration)


def play_lologro_sound():
    soundtest = os.path.join(dirname, "assets/lo-logro-senor.wav")
    duration = calculate_wav_duration(soundtest)
    winsound.PlaySound(soundtest, winsound.SND_ASYNC)
    sleep(duration)


def play_recorded_audio_test():
    audio = os.path.join(dirname, "output.wav")
    # print(audio)
    winsound.PlaySound(audio, winsound.SND_ASYNC)


def stop_recorded_audio_test():
    winsound.PlaySound(None, winsound.SND_PURGE)


def open_record_config():
    os.popen("rundll32.exe Shell32.dll,Control_RunDLL Mmsys.cpl,,1")
