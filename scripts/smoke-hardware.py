"""Read-only hardware smoke test. Reports counts, never serial numbers."""
from collections import Counter
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.hardware import HardwareClient


def main():
    client = HardwareClient()
    snapshots = []
    try:
        for operation in ("inventory", "sample", "sample"):
            snapshot = client.request(operation)
            snapshots.append({"operation": operation, "devices": dict(Counter(d.kind for d in snapshot.devices)),
                              "readings": len(snapshot.readings),
                              "available_readings": sum(r.value is not None and not r.is_stale() for r in snapshot.readings),
                              "errors": [dict(provider=e.provider, code=e.code, message=e.message) for e in snapshot.errors]})
            time.sleep(1)
        models = {kind: sorted({d.name for d in snapshot.devices if d.kind == kind}) for kind in ("cpu", "gpu", "disk", "board")}
        print(json.dumps({"models": models, "samples": snapshots}, ensure_ascii=False, indent=2))
    finally:
        client.close()


if __name__ == "__main__":
    main()
