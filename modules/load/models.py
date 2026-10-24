from dataclasses import asdict, dataclass
import math


@dataclass(frozen=True)
class LoadConfig:
    cpu_target: int = 20
    gpu_target: int = 0
    initial_cores: int = 0
    gpu_id: str | None = None
    cpu_limit: int = 95
    gpu_limit: int = 90

    def validate(self):
        for value in (self.cpu_target, self.gpu_target):
            if not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 100:
                raise ValueError("Los objetivos deben estar entre 0 y 100 %.")
        if not isinstance(self.initial_cores, int) or self.initial_cores < 0:
            raise ValueError("Cantidad de núcleos inválida.")
        if self.gpu_target and not self.gpu_id:
            raise ValueError("Selecciona una GPU para generar carga gráfica.")
        if not 40 <= self.cpu_limit <= 110 or not 40 <= self.gpu_limit <= 110:
            raise ValueError("Los límites térmicos deben estar entre 40 y 110 °C.")
        return self

    def wire(self):
        return {key: value for key, value in asdict(self).items() if key not in {"cpu_limit", "gpu_limit"}}


@dataclass(frozen=True)
class BatteryConfig:
    mode: str = "timed"
    duration_minutes: int = 120
    minimum_remaining: int = 20
    cutoff: int = 10
    brightness: int = 100

    def validate(self):
        if self.mode not in {"timed", "exhaustive", "intensive"} or self.duration_minutes < 1:
            raise ValueError("Modo o duración inválidos.")
        if not 0 <= self.minimum_remaining <= 100 or not 1 <= self.cutoff <= 99 or not 0 <= self.brightness <= 100:
            raise ValueError("La configuración de batería no es válida.")
        return self


class QualityTracker:
    def __init__(self):
        self.last = 0.0
        self.evaluated = 0.0
        self.compliant = 0.0
        self.missing_samples = 0
        self.outside_samples = 0

    def observe(self, elapsed, sample, config):
        weight = max(0, elapsed - max(15.0, self.last))
        self.last = elapsed
        if not (config.cpu_target or config.gpu_target):
            return
        self.evaluated += weight
        def matches(key, target, tolerance):
            value = sample.get(key)
            return not target or (isinstance(value, (int, float)) and math.isfinite(value) and abs(value - target) <= tolerance)
        matched = matches("cpu_actual", config.cpu_target, 5) and matches("gpu_actual", config.gpu_target, 10)
        if weight and any(target and not isinstance(sample.get(key), (int, float)) for key, target in (("cpu_actual", config.cpu_target), ("gpu_actual", config.gpu_target))):
            self.missing_samples += 1
        elif weight and not matched:
            self.outside_samples += 1
        if matched:
            # A delayed/missing sample cannot certify the entire unobserved interval.
            self.compliant += min(weight, 1.25)

    def result(self, config):
        applies = bool(config.cpu_target or config.gpu_target)
        ratio = self.compliant / self.evaluated if self.evaluated else None
        return {"applicable": applies, "valid": not applies or (ratio is not None and ratio >= .9),
                "compliance_percent": ratio * 100 if ratio is not None else None, "evaluated_seconds": self.evaluated,
                "compliant_seconds": self.compliant, "missing_samples": self.missing_samples, "outside_samples": self.outside_samples}


class BatteryFlow:
    """Pure battery rules; elapsed is monotonic wall time, never a loop count."""
    def __init__(self, config):
        self.config = config.validate()
        self.ids = None
        self.identities = {}

    def preflight(self, battery):
        if battery is None:
            raise ValueError("Batería no instalada.")
        if battery.power_plugged:
            raise ValueError("Desconecta el cargador antes de iniciar la prueba.")
        if not isinstance(battery.percent, (int, float)) or not math.isfinite(battery.percent) or not 0 <= battery.percent <= 100:
            raise ValueError("La carga de batería no es una medición válida.")
        minimum = self.config.minimum_remaining if self.config.mode == "timed" else self.config.cutoff
        if battery.percent <= minimum:
            raise ValueError(f"La carga inicial debe superar el {minimum} %.")

    def check(self, battery, elapsed, ids=None, identities=None):
        if battery is None:
            return "interrupted", "Batería retirada o medición perdida."
        if battery.power_plugged:
            return "interrupted", "Se conectó el cargador."
        if not isinstance(battery.percent, (int, float)) or not math.isfinite(battery.percent) or not 0 <= battery.percent <= 100:
            return "interrupted", "Se perdió la medición válida de batería."
        if ids is not None:
            if self.ids is None:
                self.ids = ids
            elif self.ids != ids:
                return "interrupted", "Cambió el conjunto de baterías instaladas."
        for device_id, fields in (identities or {}).items():
            known = self.identities.setdefault(device_id, {})
            for key, value in fields.items():
                if key in known and known[key] != value:
                    return "interrupted", "Cambió la identidad de una batería instalada."
                known[key] = value
        if self.config.mode == "timed":
            if battery.percent < self.config.minimum_remaining:
                return "failed", "La batería bajó del remanente mínimo antes de completar la prueba."
            if elapsed >= self.config.duration_minutes * 60:
                return "passed", "Se completó la duración con el remanente mínimo requerido."
        elif battery.percent <= self.config.cutoff:
            return "completed", "Medición de autonomía completada al alcanzar el porcentaje de corte."
        return None
