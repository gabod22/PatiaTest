import subprocess
from os import path
from time import sleep
import sys
import xmltodict
from ..constants import programs_path


def kill_process_by_name(name):
    subprocess.run("taskkill /IM " + name + " /F")


def get_gpuz_info():
    xmlfile = path.join(programs_path, "gpuz.xml")

    gpus = []
    print("Obteniendo info de las GPUs")
    # dev = getenv("DEV_MODE")
    gpuz_command = "gpuz.exe"

    try:
        command = f'"{path.join(
            programs_path, gpuz_command)}" /minimized /dump "{xmlfile}"'
        print(command)
        status = subprocess.call(command)
        print(status)
    except Exception as e:
        print("GPUZ error", e)

    if status != 0:
        raise Exception("DiskInfo.exe exited with status code " + status)

    # read data
    input_data = None
    try:
        with open(xmlfile, "r", encoding="utf-8") as f:
            input_data = f.read()
            parsed_info = xmltodict.parse(input_data)

            graphic_cards = parsed_info["gpuz_dump"]["card"]
            if type(graphic_cards) == dict:
                graphic_cards = [graphic_cards]
    except Exception as e:
        print(e)

    for card in graphic_cards:
        # clean_card = {key: card[key] for key in card.keys()
        #               & {'cardname', 'vendor', 'memsize', 'memtype'}}
        gpus.append(
            [card["cardname"], card["vendor"], card["memsize"], card["memtype"]]
        )

    return gpus
