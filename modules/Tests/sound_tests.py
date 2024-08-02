import os

import winsound
from modules.constants import dirname

from ..helpers.helpers import calculate_wav_duration
from time import sleep

# Sound tests
def play_speaker_test_sound():
    soundtest = os.path.join(dirname, "assets/soundtest.wav")
    
    winsound.PlaySound(soundtest, winsound.SND_ASYNC)
    


def stop_speaker_test_sound():
    winsound.PlaySound(None, winsound.SND_PURGE)


def play_cansado_sound():
    soundtest = os.path.join(dirname, "assets/failure.wav")
    duration = calculate_wav_duration(soundtest)
    winsound.PlaySound(soundtest, winsound.SND_ASYNC)
    sleep(duration)


def play_lologro_sound():
    soundtest = os.path.join(dirname, "assets/success.wav")
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