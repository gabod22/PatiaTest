"""Build small immutable display frames in the monitoring thread, without Qt widgets."""
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
import threading

from .formatting import format_field
from .models import Device, Field, SensorHistory, Snapshot


# Ordered, deliberately short lists for a technician's inspection.
DETAIL_FIELDS = {
    "battery": ("name", "manufacturer", "serial", "health", "full_capacity", "design_capacity", "cycles", "charge", "power_state"),
    "disk": ("model", "serial", "capacity", "interface", "volumes", "health_status", "life_remaining", "temperature", "host_reads", "host_writes", "power_on_hours", "power_on_count"),
    "cpu": ("name", "cores", "threads", "max_clock"),
    "memory": ("slot", "capacity", "type", "configured_speed", "manufacturer"),
    "board": ("manufacturer", "model"),
    "bios": ("version", "release_date"),
    "gpu": ("name", "manufacturer", "dedicated_memory", "shared_memory", "memory_type", "driver_version"),
    "gpu_vendor": ("memory_type", "dedicated_memory", "vbios"),
}
LABELS = {
    "name": "Modelo", "model": "Modelo", "manufacturer": "Fabricante", "serial": "Número de serie",
    "health": "Salud", "full_capacity": "Capacidad de carga completa", "design_capacity": "Capacidad de diseño",
    "cycles": "Ciclos", "charge": "Carga actual", "power_state": "Alimentación", "capacity": "Capacidad",
    "interface": "Interfaz", "volumes": "Volúmenes", "health_status": "Estado de salud", "life_remaining": "Vida restante estimada",
    "temperature": "Temperatura", "host_reads": "Lecturas acumuladas", "host_writes": "Escrituras acumuladas",
    "power_on_hours": "Horas encendido", "power_on_count": "Encendidos", "cores": "Núcleos", "threads": "Hilos",
    "max_clock": "Frecuencia máxima nominal", "slot": "Ranura", "type": "Tipo", "configured_speed": "Velocidad configurada",
    "nominal_speed": "Velocidad nominal",
    "version": "Versión de BIOS", "release_date": "Fecha de BIOS", "dedicated_memory": "Memoria gráfica dedicada",
    "shared_memory": "Memoria compartida máxima", "memory_type": "Tipo de memoria gráfica", "driver_version": "Controlador", "vbios": "VBIOS",
}
GROUPS = ({"battery"}, {"disk"}, {"cpu", "memory", "board", "bios"}, {"gpu", "gpu_vendor"})


@dataclass(frozen=True)
class DisplayRow:
    key: str
    values: tuple[str, ...]
    tooltip: str = ""
    expires_at: datetime | None = None


@dataclass(frozen=True)
class DisplayFrame:
    snapshot: Snapshot
    details: tuple[tuple[DisplayRow, ...], ...]
    sensors: tuple[DisplayRow, ...]
    status: str
    status_tooltip: str


class LatestFrame:
    """A single replaceable frame; a busy GUI never accumulates queued snapshots."""
    def __init__(self):
        self._lock = threading.Lock()
        self._frame = None

    def publish(self, frame):
        with self._lock:
            self._frame = frame

    def take(self):
        with self._lock:
            frame, self._frame = self._frame, None
            return frame


def compact_device(device):
    keys = DETAIL_FIELDS.get(device.kind, ())
    fields = {key: device.fields.get(key, Field()) for key in keys}
    if device.kind == "memory" and fields["configured_speed"].value is None:
        nominal = device.fields.get("nominal_speed", Field())
        if nominal.value is not None:
            fields.pop("configured_speed")
            fields["nominal_speed"] = nominal
    if device.kind in {"cpu", "gpu", "battery"} and fields["name"].value is None:
        fields["name"] = Field(device.name, source="Inventario", availability="available")
    if device.kind == "disk":
        if fields["model"].value is None:
            fields["model"] = Field(device.name, source="Inventario", availability="available")
        if fields["life_remaining"].value is None:
            fields.pop("life_remaining")  # No generic percentage for HDDs or unknown SSD wear.
    return replace(device, fields=fields)


def _preferred(readings, names, maximum=1):
    """Prefer useful package/overall sensors, including an explicit unavailable reading."""
    ranked = sorted(readings, key=lambda r: (
        r.value is None or r.availability != "available" or r.is_stale(),
        next((i for i, name in enumerate(names) if name in r.name.casefold()), len(names)), r.id))
    return ranked[:maximum]


def useful_readings(snapshot):
    devices = {device.id: device for device in snapshot.devices}
    grouped = {}
    for reading in snapshot.readings:
        grouped.setdefault(reading.device_id, []).append(reading)
    selected = []
    for device_id, readings in grouped.items():
        device = devices.get(device_id)
        kind = device.kind if device else ""
        if kind == "sensor_cpu":
            selected += _preferred([r for r in readings if r.unit == "°C"], ("package", "tctl", "tdie", "core max"))
            selected += _preferred([r for r in readings if r.unit == "%" and "total" in r.name.casefold()], ("cpu total",))
            selected += _preferred([r for r in readings if r.unit == "W"], ("package", "cores"))
            clocks = [r for r in readings if r.unit == "MHz" and "core" in r.name.casefold() and r.value is not None
                      and r.availability == "available" and not r.is_stale()]
            if clocks:
                selected.append(replace(clocks[0], id=device_id + ":average_clock", name="Frecuencia media de núcleos",
                                        value=sum(r.value for r in clocks) / len(clocks), timestamp=min(r.timestamp for r in clocks)))
        elif kind in {"sensor_gpu", "gpu", "gpu_vendor"}:
            selected += _preferred([r for r in readings if r.unit == "°C"], ("core", "gpu", "hot spot", "memory"), 2)
            selected += _preferred([r for r in readings if r.unit == "%" and any(x in r.name.casefold() for x in ("core", "3d", "total"))], ("core", "3d", "total"))
            selected += _preferred([r for r in readings if r.unit == "MHz" and "memory" not in r.name.casefold()], ("core", "gpu"))
            selected += _preferred([r for r in readings if r.unit == "W"], ("package", "power"))
            selected += _preferred([r for r in readings if r.unit in {"MiB", "GiB"} and "used" in r.name.casefold()], ("memory used",))
        elif kind in {"sensor_memory", "memory"}:
            if "virtual" in device.name.casefold() or "virtual" in device.id.casefold():
                continue
            selected += [r for r in readings if r.unit == "°C" and not any(x in r.name.casefold() for x in ("limit", "resolution"))]
            selected += _preferred([r for r in readings if r.unit == "%"], ("memory",))
            selected += _preferred([r for r in readings if r.unit == "GiB" and "used" in r.name.casefold()], ("used",))
        elif kind == "disk":
            selected += [r for r in readings if r.unit in {"°C", "B/s"}]
        elif kind in {"sensor_board", "board"}:
            selected += [r for r in readings if r.unit == "RPM"]
            selected += _preferred([r for r in readings if r.unit == "°C"], ("cpu", "system", "motherboard"), 2)
        elif kind == "battery":
            selected += [r for r in readings if r.unit in {"%", "°C", "mW"}]
        elif not device:  # Preserve explicit readings from a provider with no inventory yet.
            selected += [r for r in readings if r.unit in {"°C", "%", "B/s"}]
    return tuple(selected)


def sensor_label(reading, kind):
    name = reading.name.casefold()
    if kind == "sensor_cpu":
        return {"°C": "Temperatura CPU", "%": "Uso de CPU", "W": "Potencia CPU", "MHz": "Frecuencia media CPU"}.get(reading.unit, reading.name)
    if kind in {"sensor_gpu", "gpu", "gpu_vendor"}:
        if reading.unit == "°C":
            return "Temperatura memoria GPU" if "memory" in name else "Punto caliente GPU" if "hot" in name else "Temperatura GPU"
        return {"%": "Uso de GPU", "W": "Potencia GPU", "MHz": "Frecuencia GPU", "GiB": "Memoria gráfica en uso",
                "MiB": "Memoria compartida en uso" if "shared" in name else "Memoria gráfica en uso"}.get(reading.unit, reading.name)
    if kind in {"sensor_memory", "memory"}:
        return {"%": "Uso de RAM", "GiB": "RAM en uso", "°C": "Temperatura RAM"}.get(reading.unit, reading.name)
    return reading.name


class FrameBuilder:
    def __init__(self):
        self.history = SensorHistory()

    def build(self, snapshot):
        inventory = list(snapshot.devices)
        if not any(d.kind == "cpu" for d in inventory):
            inventory += [Device(d.id + ":identity", "cpu", d.name, {}) for d in snapshot.devices if d.kind == "sensor_cpu"]
        devices = tuple(compact_device(device) for device in inventory if device.kind in DETAIL_FIELDS)
        readings = useful_readings(snapshot)
        self.history.update(readings)
        details = []
        for kinds in GROUPS:
            rows = []
            for device in devices:
                if device.kind not in kinds:
                    continue
                for key, field in device.fields.items():
                    # Optional unknown metadata should not drown useful facts in placeholders.
                    if field.value is None and key not in {"name", "model", "capacity", "health", "health_status", "type", "configured_speed"}:
                        continue
                    text = ", ".join(map(str, field.value)) if isinstance(field.value, list) else format_field(field)
                    rows.append(DisplayRow(device.id + ":" + key, (device.name, LABELS[key], text),
                                           " · ".join(filter(None, (field.source, field.reason)))))
            details.append(tuple(rows))
        names = {d.id: d.name for d in snapshot.devices}
        kinds = {d.id: d.kind for d in snapshot.devices}
        sensors = []
        number = lambda value: "—" if value is None else f"{value:.2f}"
        for reading in readings:
            stale = reading.is_stale()
            low, high = self.history.extrema.get(reading.id, (None, None))
            state = "Caducada" if stale else "Disponible" if reading.value is not None and reading.availability == "available" else "No disponible"
            expires = reading.timestamp + timedelta(seconds=65 if reading.source == "SMART" else 5)
            sensors.append(DisplayRow(reading.id, (names.get(reading.device_id, "Componente"), sensor_label(reading, kinds.get(reading.device_id)),
                                                  number(reading.value) if state == "Disponible" else "—",
                                                  number(low), number(high), reading.unit, state),
                                      " · ".join(filter(None, (reading.name, reading.source, reading.reason, reading.timestamp.astimezone().strftime("%H:%M:%S")))), expires))
        kinds_present = {d.kind for d in snapshot.devices}
        temperatures = {r.device_id for r in readings if r.unit == "°C"}
        for device in snapshot.devices:
            if device.kind not in {"cpu", "memory", "gpu", "disk", "sensor_cpu", "sensor_memory", "sensor_gpu"}:
                continue
            if device.kind in {"cpu", "memory", "gpu"} and "sensor_" + device.kind in kinds_present:
                continue
            if device.id not in temperatures and "virtual" not in device.name.casefold():
                sensors.append(DisplayRow(device.id + ":missing_temperature", (device.name, "Temperatura", "—", "—", "—", "°C", "No disponible"),
                                          "El sensor no está expuesto o necesita preparar el acceso al hardware."))
        errors = list(dict.fromkeys(error.message for error in snapshot.errors))
        notices = errors[:2] + ([f"{len(errors) - 2} avisos adicionales; ver detalle al pasar el cursor."] if len(errors) > 2 else [])
        status = " · ".join(notices) if notices else "Monitoreo activo. Actualización cada segundo."
        return DisplayFrame(Snapshot(devices, readings, snapshot.errors), tuple(details), tuple(sensors), status,
                            "\n".join(f"{e.provider}: {e.message}" for e in snapshot.errors))
