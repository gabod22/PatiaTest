"""Owned load helper with bounded IPC and a kill-on-close Windows Job Object."""
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import uuid


class LoadError(RuntimeError):
    pass


def command():
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    candidates = [root / "runtime/load/PatiaLoadHost.exe"]
    if not getattr(sys, "frozen", False):
        candidates += [root / f"native/PatiaLoadHost/bin/{mode}/net10.0-windows/win-x64/PatiaLoadHost.exe" for mode in ("Release", "Debug")]
    for path in candidates:
        if path.is_file():
            return [str(path)]
    raise LoadError("Falta PatiaLoadHost; ejecuta scripts/build-load.ps1.")


class LoadClient:
    def __init__(self, cmd=None):
        self.cmd = cmd
        self.process = None
        self.job = None
        self.messages = queue.Queue()
        self.reader = None

    def _start(self):
        if self.process is not None:
            if self.process.poll() is not None:
                raise LoadError("El motor de carga se cerró inesperadamente.")
            return
        self.process = subprocess.Popen(self.cmd or command(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL, text=True, encoding="utf-8", bufsize=1,
                                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        if os.name == "nt":
            try:
                import win32job
                self.job = win32job.CreateJobObject(None, "")
                info = win32job.QueryInformationJobObject(self.job, win32job.JobObjectExtendedLimitInformation)
                info["BasicLimitInformation"]["LimitFlags"] = win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
                win32job.SetInformationJobObject(self.job, win32job.JobObjectExtendedLimitInformation, info)
                win32job.AssignProcessToJobObject(self.job, int(self.process._handle))
            except Exception as error:
                self.close()
                raise LoadError("No se pudo proteger el proceso de carga con un Job Object: " + str(error)) from error
        process = self.process
        messages = self.messages
        def read():
            try:
                for line in process.stdout:
                    messages.put(line)
            except (OSError, ValueError):
                pass
            finally:
                messages.put(None)
        self.reader = threading.Thread(target=read, daemon=True, name="PatiaLoadReader")
        self.reader.start()

    def request(self, operation, config=None):
        try:
            self._start()
            id = uuid.uuid4().hex
            request = {"version": 1, "id": id, "operation": operation}
            if config is not None:
                request["config"] = config.wire()
            self.process.stdin.write(json.dumps(request) + "\n")
            self.process.stdin.flush()
            line = self.messages.get(timeout=12 if operation in {"start", "update"} else 4)
            if line is None:
                raise LoadError("El motor de carga se cerró o perdió la comunicación.")
            response = json.loads(line)
            if response.get("version") != 1 or response.get("id") != id or response.get("operation") != operation:
                raise LoadError("Respuesta del motor incompatible o fuera de secuencia.")
            if not response.get("ok"):
                raise LoadError(response.get("error", "Falló el motor de carga."))
            return response["data"]
        except (OSError, ValueError, KeyError, TypeError, queue.Empty) as error:
            raise LoadError(str(error) or "Tiempo de espera de carga agotado.") from error

    def close(self):
        process, self.process = self.process, None
        if process:
            if process.poll() is None:
                process.kill()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                pass
            for pipe in (process.stdin, process.stdout):
                if pipe:
                    pipe.close()
        if self.job:
            self.job.Close()
            self.job = None
        if self.reader:
            self.reader.join(timeout=1)
            self.reader = None
