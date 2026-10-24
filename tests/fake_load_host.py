import json
import sys
import time

mode = sys.argv[1]
for line in sys.stdin:
    request = json.loads(line)
    if mode == "hang":
        time.sleep(20)
    if mode == "crash":
        sys.exit(2)
    response = {**request, "ok": True, "data": {"state": "stopped"}}
    if mode == "bad_version": response["version"] = 2
    if mode == "bad_id": response["id"] = "other"
    if mode == "error": response.update(ok=False, error="adapter disappeared")
    print(json.dumps(response), flush=True)
