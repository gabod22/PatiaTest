"""Basic startup summary. Detailed hardware inventory is owned by modules.hardware."""
import platform
import cpuinfo
import cv2
import psutil
import pythoncom
import wmi
from cv2_enumerate_cameras import enumerate_cameras
from modules.helpers.system_accions import get_registry_value
from modules.utils import convert_size, wmiToDict

MemoryType = {0: "Desconocido", 1: "Otro", 20: "DDR", 21: "DDR2", 22: "DDR2 FB-DIMM", 24: "DDR3", 26: "DDR4", 34: "DDR5", 35: "LPDDR5"}


def get_system_info(progress_callback, on_error, show_dialog):
    pythoncom.CoInitialize()
    info = {"cameras": [], "computer_system": {}, "bios": {}, "cpu": {}, "memories": [],
            "virtual_memory": dict(psutil.virtual_memory()._asdict()), "winver": platform.platform()}
    def query(key, callback):
        progress_callback.emit("Obteniendo información: " + key)
        try:
            info[key] = callback()
        except Exception as error:
            on_error.emit(f"{key}: {error}")
    try:
        query("cameras", lambda: enumerate_cameras(cv2.CAP_MSMF))
        query("cpu", cpuinfo.get_cpu_info)
        query("winver", lambda: os_version(progress_callback))
        try:
            connection = wmi.WMI()
        except Exception as error:
            on_error.emit(f"WMI: {error}")
            return info
        query("computer_system", lambda: dict(wmiToDict(connection.Win32_ComputerSystem()[0])))
        def bios():
            row = connection.Win32_BIOS()[0]
            return {"Manufacturer": row.Manufacturer, "Version": row.SMBIOSBIOSVersion,
                    "ReleaseDate": row.ReleaseDate, "SerialNumber": row.SerialNumber}
        query("bios", bios)
        query("memories", lambda: getMemory(progress_callback, connection))
    finally:
        pythoncom.CoUninitialize()
    return info


def getMemory(progress_callback, wmi):
    return [{"capacidad": convert_size(row.Capacity), "Tipo": MemoryType.get(row.SMBIOSMemoryType, "Desconocido"),
             "Frecuencia": row.Speed, "Fabricante": row.Manufacturer,
             "Referencia": row.PartNumber, "Serie": row.SerialNumber, "Ranura": row.DeviceLocator,
             "FrecuenciaConfigurada": getattr(row, "ConfiguredClockSpeed", None)} for row in wmi.Win32_PhysicalMemory()]


def os_version(progress_callback):
    def get(key):
        return get_registry_value("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", key)
    return f"{get('ProductName')} (build {get('DisplayVersion')})"
