"""A separate process exercising the real client framing and lifecycle."""
import json
import sys
import time


def main():
    mode = sys.argv[1]
    for line in sys.stdin:
        request = json.loads(line)
        if request["operation"] == "shutdown":
            break
        if mode == "hang":
            time.sleep(10)
        if mode == "crash":
            return
        if mode == "malformed":
            print("not-json", flush=True)
            continue
        response = dict(version=1, id=request["id"], operation=request["operation"], devices=[], readings=[], errors=[])
        if mode == "bad_id":
            response["id"] = "another-request"
        elif mode == "bad_version":
            response["version"] = 2
        elif mode == "partial":
            response["devices"] = [{"id": "disk:1", "kind": "disk", "name": "USB", "fields": {"health_status": {"value": None, "availability": "unavailable", "reason": "No SMART"}}}]
            response["errors"] = [{"provider": "storage", "code": "unsupported", "message": "No SMART"}]
        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
