"""Session-scoped sleep inhibition and reversible brightness, without powercfg changes."""
import ctypes
import os


class PowerSession:
    def __init__(self, brightness=None):
        self.brightness = brightness
        self.previous = []
        self.warning = None

    def __enter__(self):
        if os.name != "nt":
            return self
        if not ctypes.windll.kernel32.SetThreadExecutionState(0x80000003):
            raise OSError("No se pudo impedir la suspensión automática durante la prueba.")
        if self.brightness is not None:
            try:
                import wmi
                connection = wmi.WMI(namespace="root/WMI")
                levels = {row.InstanceName: row.CurrentBrightness for row in connection.WmiMonitorBrightness() if row.Active}
                for method in connection.WmiMonitorBrightnessMethods():
                    if method.InstanceName in levels:
                        self.previous.append((method, levels[method.InstanceName]))
                        method.WmiSetBrightness(Brightness=int(self.brightness), Timeout=0)
                if not self.previous:
                    self.warning = "El equipo no expone control de brillo."
            except Exception as error:
                self.warning = "No se pudo fijar el brillo: " + str(error)
        return self

    def __exit__(self, *args):
        for method, previous in self.previous:
            try:
                method.WmiSetBrightness(Brightness=int(previous), Timeout=0)
            except Exception as error:
                self.warning = "No se pudo restaurar el brillo: " + str(error)
        # Release WMI proxies on the session thread before CoUninitialize.
        self.previous.clear()
        if os.name == "nt":
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
