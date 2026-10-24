"""One owned, hidden process. No shells, temporary exports or global taskkill."""
import atexit
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time
import uuid

from .models import Snapshot


class HardwareError(RuntimeError):
    pass


def host_command():
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    candidates = [root / "runtime/hardware/PatiaHardwareHost.exe"]
    if not getattr(sys, "frozen", False):
        candidates.extend(root / f"native/PatiaHardwareHost/bin/{mode}/net10.0-windows/win-x64/PatiaHardwareHost.exe"
                          for mode in ("Release", "Debug"))
    for candidate in candidates:
        if candidate.is_file():
            return [str(candidate)]
    raise HardwareError("Falta PatiaHardwareHost. Ejecuta scripts/build-hardware.ps1 antes de iniciar la aplicación.")


class HardwareClient:
    def __init__(self, command=None, timeout=5):
        self.command = command
        self.timeout = timeout
        self._lock = threading.Lock()
        self._process = None
        self._queue = None
        self._reader = None
        self._next_start = 0

    def _start(self):
        if self._process and self._process.poll() is None:
            return
        if time.monotonic() < self._next_start:
            raise HardwareError("El componente se está recuperando; se reintentará automáticamente.")
        self._dispose()
        command = self.command or host_command()
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        self._process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
                                         bufsize=1, creationflags=flags)
        messages = queue.Queue(maxsize=8)
        process = self._process
        self._queue = messages

        def read():
            try:
                while True:
                    line = process.stdout.readline(4 * 1024 * 1024 + 1)
                    if not line or len(line) > 4 * 1024 * 1024:
                        break
                    messages.put(line, timeout=1)
            except (OSError, ValueError, queue.Full):
                pass
            finally:
                try:
                    messages.put_nowait(None)
                except queue.Full:
                    pass

        self._reader = threading.Thread(target=read, name="PatiaHardwareReader", daemon=True)
        self._reader.start()

    def request(self, operation):
        if operation not in {"inventory", "sample", "refresh_devices", "shutdown"}:
            raise ValueError("Unknown hardware operation")
        with self._lock:
            try:
                self._start()
                request_id = uuid.uuid4().hex
                self._process.stdin.write(json.dumps({"version": 1, "id": request_id, "operation": operation}) + "\n")
                self._process.stdin.flush()
                line = self._queue.get(timeout=self.timeout)
                if line is None:
                    raise HardwareError("El componente de hardware se cerró inesperadamente.")
                response = json.loads(line)
                if not isinstance(response, dict) or response.get("version") != 1 or response.get("id") != request_id or response.get("operation") != operation:
                    raise HardwareError("Respuesta de hardware incompatible o fuera de secuencia.")
                return Snapshot.from_response(response)
            except (OSError, ValueError, TypeError, KeyError, queue.Empty, HardwareError) as ex:
                self._dispose()
                self._next_start = time.monotonic() + 2
                raise HardwareError(str(ex) or "Tiempo de espera de hardware agotado.") from ex

    def _dispose(self):
        process, self._process = self._process, None
        if not process:
            return
        if process.poll() is None:
            process.kill()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            pass
        for pipe in (process.stdin, process.stdout):
            if pipe:
                pipe.close()
        if self._reader and self._reader is not threading.current_thread():
            self._reader.join(timeout=1)
        self._reader = None

    def restart(self):
        with self._lock:
            self._dispose()
            self._next_start = 0

    def close(self):
        # Shutdown is bounded; kill only our child if native code is stuck.
        with self._lock:
            if self._process and self._process.poll() is None:
                try:
                    self._process.stdin.write(json.dumps({"version": 1, "id": "close", "operation": "shutdown"}) + "\n")
                    self._process.stdin.flush()
                    self._process.wait(timeout=2)
                except (OSError, subprocess.TimeoutExpired):
                    pass
            self._dispose()


client = HardwareClient()
atexit.register(client.close)
