from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import uuid


def log_root():
    return Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "PixelTest" / "tests"


class SessionLog:
    def __init__(self, config, battery=None):
        self.folder = log_root() / (datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:8])
        self.folder.mkdir(parents=True)
        self.stream = (self.folder / "samples.jsonl").open("w", encoding="utf-8")
        self.event("configuration", load=asdict(config), battery=asdict(battery) if battery else None, kernel="scalar-xorshift/d3d11-fp32-v1")

    def event(self, type, **data):
        self.stream.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(), "type": type, **data}, ensure_ascii=False, allow_nan=False) + "\n")
        self.stream.flush()

    def finish(self, result):
        try:
            (self.folder / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
        finally:
            self.stream.close()
