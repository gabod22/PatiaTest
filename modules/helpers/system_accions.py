import os
import subprocess
from pathlib import Path
from .helpers import filter_exe_files
from ..constants import programs_path

def open_program(program_name):
    """Ejecuta un programa dentro especificado

    Args:
        program (str): Ubicación absoluta del programa
    """
    
    try:
        path = os.path.join(programs_path, program_name)
        print("Abriendo el programa {0} ".format(program_name))
        os.popen(path)

    except Exception as e:
        print("No se pudo ejectutar el programa {0} por un error: {1}".format(program_name, e))

def get_all_programs(path: Path):
    """devuelve la lista de todos los ejecutables .exe de la ubicación proporcionada

    Args:
        path (Path): Ubicación absoluta de la carpeta

    Returns:
        list: Lista de todos los programas en la carpeta
    """
    entries = os.listdir(path)
    # print(entries)
    programs = list(filter(filter_exe_files, entries))
    program_list = list()
    for program in programs:
        p = dict()
        # print(os.path.join(
        #     dirname, 'programs') + "/" + program)
        # icon = extract_icon(os.path.join(
        #     dirname, 'programs') + "/" + program, IconSize.LARGE)

        # img = win32_icon_to_image(icon, IconSize.LARGE)
        p["name"] = program
        p["icon"] = None

        program_list.append(p)

    return program_list

def run_powershell_command(command):
    """Esta funcion ejecuta un comando con powershell

    Args:
        command (str): Es el comando que se va a ejecutar de powershell
    """
    subprocess.run(command, shell=True)


def kill_process_by_name(name):
    """Elimina un proceso buscandolo por el nombre

    Args:
        name (str): nombre del programa ejecutado *.exe
    """
    subprocess.run("taskkill /IM " + name + " /F")

def get_registry_value(key, subkey, value):
    """Obetiene el valor de un registro en el editor de registros 

    Args:
        key (str): Nombre de ka
        subkey (_type_): _description_
        value (_type_): _description_

    Returns:
        _type_: _description_
    """
    import winreg

    key = getattr(winreg, key)
    handle = winreg.OpenKey(key, subkey)
    (value, type) = winreg.QueryValueEx(handle, value)
    return value

def sync_date_time():
    run_powershell_command("net stop w32time")
    run_powershell_command("w32tm /unregister")
    run_powershell_command("w32tm /register")
    run_powershell_command("net start w32time")
    run_powershell_command("w32tm /resync")