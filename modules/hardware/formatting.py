import json
from .models import Field


def format_field(field):
    if field.value is None or field.availability != "available":
        return "No disponible"
    value = field.value
    if isinstance(value, bool):
        return "Sí" if value else "No"
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, indent=2)
    if field.unit == "B":
        try:
            number = int(value)
            for unit in ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"):
                if abs(number) < 1024:
                    return f"{number:.2f} {unit}" if unit != "B" else f"{number} B"
                number /= 1024
            return f"{value} B"
        except (TypeError, ValueError, OverflowError):
            pass
    if isinstance(value, float):
        value = f"{value:.2f}"
    return f"{value} {field.unit}".strip() if field.unit else str(value)


def value(device, key):
    return format_field(device.fields.get(key, Field()))
