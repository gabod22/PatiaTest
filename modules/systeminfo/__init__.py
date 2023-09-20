from ..helpers import convert_size, WMIDateStringToDate, wmiToDict
from ..DiskInfoParser import DiskInfo
import wmi

import platform
import cpuinfo
import psutil
import sys
import pythoncom
import GPUtil


def get_system_info(progress_callback, on_error):
    pythoncom.CoInitialize()
    info = dict()
    w = wmi.WMI()
    MemoryType = {
        0: "Desconocido",
        1: "Otro",
        20: "DDR",
        21: "DDR2",
        22: "DDR2 FB-DIMM",
        24: "DDR3",
        26: "DDR4",
    }
    progress_callback.emit('Obteniendo info de la plataforma')

    # INFO
    info['computer_system'] = dict(wmiToDict(w.Win32_ComputerSystem()[0]))
    # Platform
    uname_result = platform.uname()
    pl = dict()
    pl['system'] = uname_result.system
    pl['node'] = uname_result.node
    pl['release'] = uname_result.release
    pl['version'] = uname_result.version
    pl['machine'] = uname_result.machine
    info['platform'] = pl

    progress_callback.emit('Obteniendo info de la BIOS')
    # BIOS
    bios = dict()
    biosraw = w.Win32_BIOS()[0]

    bios = {
        "Manufacturer": biosraw.Manufacturer,
        "Version": biosraw.SMBIOSBIOSVersion,
        "ReleaseDate": biosraw.ReleaseDate,
        "SerialNumber": biosraw.SerialNumber,
        "Description": biosraw.Description,
        "InstallableLanguages": biosraw.InstallableLanguages,
        "LanguageEdition": biosraw.LanguageEdition,
        "Name": biosraw.Name,
        "PrimaryBIOS": biosraw.PrimaryBIOS,
        "Status": biosraw.Status,
        "caption": biosraw.caption,
    }

    info['bios'] = bios
    progress_callback.emit('Obteniendo info del CPU')
    # CPU
    cpu = dict(cpuinfo.get_cpu_info())
    cpu['processor'] = uname_result.processor
    cpu.pop('flags')
    # cpu['cpu-times'] = psutil.cpu_times()
    cpu['pyhsical-core-count'] = psutil.cpu_count(False)
    cpu['logical-core-count'] = psutil.cpu_count(True)
    # cpu['stats'] = psutil.cpu_stats()
    info['cpu'] = cpu

    progress_callback.emit('Obteniendo info de la memoria ram')
    # Memory
    info['virtual_memory'] = dict(psutil.virtual_memory()._asdict())
    info['swap_memory'] = dict(psutil.swap_memory()._asdict())
    memories = []
    for memory in w.Win32_PhysicalMemory():

        memories.append({
            "capacidad": convert_size(memory.Capacity),
            "Tipo": MemoryType[memory.SMBIOSMemoryType],
            "Frecuencia": memory.Speed,
            "Fabricante": memory.Manufacturer
        })

    info['memories'] = memories
    progress_callback.emit('Obteniendo info del disco')
    # Disk
    info['disk_partitions'] = psutil.disk_partitions()
    root_path = 'C:/' if sys.platform == 'win32' else '/'
    info['disks'] = get_disks_info(w)

    
    # total, used, free, percent
    info['disk_usage'] = dict(psutil.disk_usage(root_path)._asdict())

    progress_callback.emit('Obteniendo info de las GPUs')

    info['gpus'] = getGPUs()

    progress_callback.emit('Terminado')
    return info

def get_disks_info(w):
    disks = []
    for drive in w.query("SELECT * FROM Win32_DiskDrive"):
        if(drive.InterfaceType != 'USB'):
            disks.append(
            [drive.Caption, drive.InterfaceType, convert_size(int(drive.Size)), drive.Status]
            )
        print(disks)
    return disks
def getGPUs():
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
        # get the GPU id
        gpu_id = gpu.id
        # name of GPU
        gpu_name = gpu.name
        # get % percentage of GPU usage of that GPU
        gpu_load = f"{gpu.load*100}%"
        # get free memory in MB format
        gpu_free_memory = f"{gpu.memoryFree}MB"
        # get used memory
        gpu_used_memory = f"{gpu.memoryUsed}MB"
        # get total memory
        gpu_total_memory = (gpu.memoryTotal / 1024)
        # get GPU temperature in Celsius
        gpu_temperature = f"{gpu.temperature} C"
        gpu_uuid = gpu.uuid
        list_gpus.append([gpu_name, str(gpu_total_memory)+" GB"])
    return list_gpus
