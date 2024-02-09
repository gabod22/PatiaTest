from ..helpers import convert_size, WMIDateStringToDate, wmiToDict, get_registry_value
from ..DiskInfoParser import DiskInfo
from ..battery import get_battery_info
import wmi
import cpuinfo
import psutil
import pythoncom
from ..gpuz import get_gpuz_info

MemoryType = {
    0: "Desconocido",
    1: "Otro",
    20: "DDR",
    21: "DDR2",
    22: "DDR2 FB-DIMM",
    24: "DDR3",
    26: "DDR4",
    29: "Row of chips",
    30: "Row of chips",
    34: "DDR5"
}


def get_system_info(progress_callback, on_error, show_dialog):
    pythoncom.CoInitialize()
    info = dict()
    w = wmi.WMI()

    progress_callback.emit('Obteniendo info de la computadora')

    # INFO
    info['computer_system'] = dict(wmiToDict(w.Win32_ComputerSystem()[0]))
    # Platform
    # uname_result = platform.uname()
    # pl = dict()
    # pl['system'] = uname_result.system
    # pl['node'] = uname_result.node
    # pl['release'] = uname_result.release
    # pl['version'] = uname_result.version
    # pl['machine'] = uname_result.machine
    # info['platform'] = pl
    progress_callback.emit('Obteniendo version de windows')
    info['winver'] = os_version()

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

    # CPU
    cpu = getCpu(progress_callback)
    # cpu['stats'] = psutil.cpu_stats()
    info['cpu'] = cpu

    # Memory
    memories = getMemory(progress_callback, wmi=w)
    info['memories'] = memories
    info['virtual_memory'] = dict(psutil.virtual_memory()._asdict())
    # info['swap_memory'] = dict(psutil.swap_memory()._asdict())

    # Disk
    # info['disk_partitions'] = psutil.disk_partitions()
    # root_path = 'C:/' if sys.platform == 'win32' else '/'

    # total, used, free, percent
    # info['disk_usage'] = dict(psutil.disk_usage(root_path)._asdict())
    gpus = getGPUs(progress_callback)
    disks = getDisks(progress_callback)
    batteries = getBatteryInfo(progress_callback)

    info['gpus'] = gpus
    info['disks'] = disks
    info['batteries'] = batteries
    progress_callback.emit('Terminado')

    return info


def getGPUs(progress_callback):
    progress_callback.emit('Obteniendo info de las GPUs')
    # try:
    #     amd_cards = ADLManager.getInstance().getDevices()
    #     for gpu in amd_cards:
    #         print(gpus.adapterName)
    # except Exception as e:
    #     print(e)

    try:
        gpus = get_gpuz_info()
    except Exception as e:
        print(e)
        gpus = None
    return gpus


def getBatteryInfo(progress_callback):
    progress_callback.emit('Obteniendo info de las baterias')
    try:
        batteries = get_battery_info()
    except Exception as e:
        progress_callback.emit('Hubo un problema al cargar las baterias')
        progress_callback.emit(e)
        batteries = []
    finally:
        return batteries


def getDisks(progress_callback):
    progress_callback.emit('Obteniendo info de las unidades de almacenamiento')
    try:
        disks = DiskInfo()
    except Exception as e:
        disks = {}
        print(e)
    finally:
        return disks


def getMemory(progress_callback, wmi):
    progress_callback.emit('Obteniendo info de la memoria ram')
    memories = []
    try:
        for memory in wmi.Win32_PhysicalMemory():
            memoryType = "Desconocido"
            if type(MemoryType[memory.SMBIOSMemoryType]) == str:
                print("tipo de memoria", memory.SMBIOSMemoryType)
                memoryType = MemoryType[memory.SMBIOSMemoryType]
            memories.append({
                "capacidad": convert_size(memory.Capacity),
                "Tipo": memoryType,
                "Frecuencia": memory.Speed,
                "Fabricante": memory.Manufacturer
            })
    except Exception as e:
        print(e)
        progress_callback.emit("No se pudo obtener la info de la memoria RAM")
        memories = []
    finally:
        return memories


def getCpu(progress_callback):
    progress_callback.emit('Obteniendo info del CPU')
    try:
        cpu = dict(cpuinfo.get_cpu_info())
        # cpu['processor'] = uname_result.processor
        # cpu.pop('flags')
        # cpu['cpu-times'] = psutil.cpu_times()
        # cpu['pyhsical-core-count'] = psutil.cpu_count(False)
        # cpu['logical-core-count'] = psutil.cpu_count(True)

    except:
        cpu = {}
    finally:
        return cpu


def os_version():
    def get(key):
        return get_registry_value(
            "HKEY_LOCAL_MACHINE",
            "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
            key)
    os = get("ProductName")
    # sp = get("CSDVersion")
    build = get("DisplayVersion")
    return "%s (build %s)" % (os, build)
