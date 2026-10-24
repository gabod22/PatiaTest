"""Explicit, bounded physical load validation. Always stops its own helper."""
import argparse
import json
from pathlib import Path
import statistics
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules.load.client import LoadClient
from modules.load.models import LoadConfig, QualityTracker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpu", type=int, default=20)
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--seconds", type=int, default=300)
    parser.add_argument("--cores", type=int, default=1)
    parser.add_argument("--output", default="build/load-validation.json")
    args = parser.parse_args()
    client = LoadClient()
    samples = []
    quality = QualityTracker()
    try:
        cap = client.request("capabilities")
        config = LoadConfig(args.cpu, args.gpu, args.cores, cap["gpus"][0]["id"] if cap["gpus"] else None).validate()
        client.request("start", config)
        start = time.monotonic()
        while time.monotonic() - start < args.seconds:
            time.sleep(1)
            sample = client.request("status")
            elapsed = time.monotonic() - start
            quality.observe(elapsed, sample, config)
            samples.append({"elapsed": elapsed, **sample})
            if len(samples) % 30 == 0:
                print(f"{elapsed:.0f}s CPU={sample['cpu_actual']} GPU={sample['gpu_actual']} núcleos={sample['active_cores']}", flush=True)
        result = {"config": config.wire(), "quality": quality.result(config), "samples": samples}
        output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result["quality"]), flush=True)
    finally:
        try:
            client.request("stop")
        finally:
            client.close()


if __name__ == "__main__":
    main()
