"""Real UI/helper session with zero generated load and workspace-only test logs."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
import sys
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
import PixelTest


def main():
    app = QApplication.instance() or QApplication([])
    with patch.object(PixelTest.MainWindow, "start_loading_dialog"), \
         patch("modules.load.logging.log_root", return_value=Path("build/load-ui-records")):
        window = PixelTest.MainWindow()
        window.resize(1100, 800)
        window.ui.tabWidget.setCurrentWidget(window.ui.tabLoad)
        panel = window.load_panel
        panel.controls.ui.CpuTarget.setCurrentText("0")
        panel.controls.ui.GpuTarget.setCurrentText("0")
        window.show()
        QTimer.singleShot(700, panel.start_standalone)
        QTimer.singleShot(5500, window.close)
        app.exec()
        assert panel.session is None, "Session thread did not stop"
        assert not panel.probe.isRunning(), "Probe did not stop"
        assert not window.hardware_panel.thread.isRunning(), "Hardware worker did not stop"
        assert panel.last_result and panel.last_result["status"] == "cancelled", panel.last_result
        folder = Path(panel.last_result["log_folder"])
        assert (folder / "summary.json").is_file()
        assert '"type": "sample"' in (folder / "samples.jsonl").read_text(encoding="utf-8")
        print("PASS: real UI/helper session, sample logs, async close and single cancellation result")


if __name__ == "__main__":
    main()
