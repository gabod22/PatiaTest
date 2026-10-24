"""Battery presence for existing tests; detailed inventory uses hardware IOCTLs."""
import psutil


def is_battery_installed():
    return psutil.sensors_battery() is not None
