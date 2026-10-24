"""Exercise the real main window without Wi-Fi, power-plan or camera side effects."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
import sys
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QApplication
import PixelTest


def main():
    app = QApplication.instance() or QApplication([])
    # The offscreen plugin cannot enumerate Windows fonts in the sandbox.
    QFontDatabase.addApplicationFont("C:/Windows/Fonts/segoeui.ttf")
    app.setFont(QFont("Segoe UI", 10))
    with patch.object(PixelTest, "set_showroom_configuration"), patch.object(PixelTest, "set_brightness"), \
         patch.object(PixelTest.MainWindow, "start_loading_dialog"), patch.object(PixelTest, "sleep"):
        window = PixelTest.MainWindow()
        window.resize(1100, 800)
        window.hardware_panel.open_details(4)
        window.show()
        def finish():
            output = Path("build/hardware-ui.png")
            output.parent.mkdir(exist_ok=True)
            window.grab().save(str(output))
            print("Sensor rows:", window.hardware_panel.ui.SensorReadings.model().rowCount())
            print("UI snapshot:", output)
            window.close()
        QTimer.singleShot(6000, finish)
        app.exec()
        assert not window.hardware_panel.thread.isRunning(), "Hardware thread did not terminate"
        print("PASS: main window rendered and closed cleanly")


if __name__ == "__main__":
    main()
