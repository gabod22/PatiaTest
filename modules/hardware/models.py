"""Typed wire models. Values remain numeric; formatting belongs to the UI."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import math
import re


def timestamp(value: str) -> datetime:
    # .NET emits 100 ns precision; Python 3.10 accepts at most microseconds.
    value = re.sub(r"\.(\d+)", lambda match: "." + match[1][:6].ljust(6, "0"), value)
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Hardware timestamps must include a timezone")
    return parsed


@dataclass(frozen=True)
class Field:
    value: Any = None
    unit: Optional[str] = None
    source: str = ""
    availability: str = "unavailable"
    reason: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or data.get("availability", "unavailable") not in {"available", "unavailable", "stale"}:
            raise ValueError("Invalid field")
        if isinstance(data.get("value"), float) and not math.isfinite(data["value"]):
            raise ValueError("Invalid numeric field")
        values = {k: data[k] for k in cls.__dataclass_fields__ if k in data}
        # The native JSON serializer sends 128-bit counters as decimal strings.
        # Restore exact integers before any formatting or arithmetic in Python.
        if str(values.get("source", "")).startswith("NVMe") and isinstance(values.get("value"), str) and values["value"].isdigit():
            values["value"] = int(values["value"])
        return cls(**values)


@dataclass(frozen=True)
class Device:
    id: str
    kind: str
    name: str
    fields: dict[str, Field] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or not isinstance(data.get("fields"), dict) or not all(isinstance(data.get(k), str) for k in ("id", "kind", "name")):
            raise ValueError("Invalid device")
        return cls(data["id"], data["kind"], data["name"],
                   {key: Field.from_dict(value) for key, value in data["fields"].items()})


@dataclass(frozen=True)
class Reading:
    id: str
    device_id: str
    name: str
    value: Optional[float]
    unit: str
    source: str
    timestamp: datetime
    availability: str = "available"
    reason: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        values = dict(data)
        values["timestamp"] = timestamp(values["timestamp"])
        value = values.get("value")
        if value is not None and (not isinstance(value, (int, float)) or not math.isfinite(value)):
            raise ValueError("Invalid sensor value")
        return cls(**values)

    def is_stale(self, now=None):
        age = ((now or datetime.now(timezone.utc)) - self.timestamp).total_seconds()
        return age > (65 if self.source == "SMART" else 5) or age < -5


@dataclass(frozen=True)
class ProviderError:
    provider: str
    code: str
    message: str


@dataclass(frozen=True)
class Snapshot:
    devices: tuple[Device, ...] = ()
    readings: tuple[Reading, ...] = ()
    errors: tuple[ProviderError, ...] = ()

    @classmethod
    def from_response(cls, data):
        if not all(isinstance(data.get(k), list) for k in ("devices", "readings", "errors")):
            raise ValueError("Invalid hardware response")
        # WMI inventories every visible disk; SMART enriches it only when available.
        merged = {}
        for raw in data["devices"]:
            device = Device.from_dict(raw)
            previous = merged.get(device.id)
            if previous:
                fields = dict(previous.fields)
                fields.update({key: value for key, value in device.fields.items()
                               if (value.value is not None and value.availability == "available") or key not in fields})
                device = Device(device.id, device.kind, device.name or previous.name, fields)
            merged[device.id] = device
        # WMI and the storage toolkit can use different paths for the same disk.
        by_path = {}
        for device in list(merged.values()):
            if device.kind != "disk":
                continue
            path = str(device.fields.get("path", Field()).value or device.id).casefold()
            previous = by_path.get(path)
            if previous:
                fields = dict(previous.fields)
                fields.update({k: v for k, v in device.fields.items() if (v.value is not None and v.availability == "available") or k not in fields})
                merged.pop(previous.id, None)
                device = Device(device.id, device.kind, device.name, fields)
                merged[device.id] = device
            by_path[path] = device
        return cls(tuple(merged.values()), tuple(Reading.from_dict(x) for x in data["readings"]),
                   tuple(ProviderError(**x) for x in data["errors"]))


class SensorHistory:
    def __init__(self):
        self.extrema = {}
        self.last_seen = {}

    def update(self, readings):
        for reading in readings:
            if reading.value is None or reading.availability != "available" or reading.is_stale():
                continue
            # Cached SMART samples must not be mistaken for fresh observations.
            if self.last_seen.get(reading.id) == reading.timestamp:
                continue
            lo, hi = self.extrema.get(reading.id, (reading.value, reading.value))
            self.extrema[reading.id] = (min(lo, reading.value), max(hi, reading.value))
            self.last_seen[reading.id] = reading.timestamp

    def reset(self):
        self.extrema.clear()
        self.last_seen.clear()
