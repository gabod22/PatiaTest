import cv2
import qimage2ndarray
from PySide6.QtCore import QThreadPool, QThread, QTimer, QSize, Qt
from PySide6.QtGui import QImage

from PySide6.QtCore import Signal, QObject
import psutil
from modules.helpers import secs2hours
from time import sleep

DEFAULT_TIME = 60
TOTAL_CPU = psutil.cpu_count(logical=True)
PERCENT = 100


class CameraCapture(QObject):

    finished = Signal()  # signals to communicate with main
    imageUpdate = Signal(QImage)  # should be class attributes
    onError = Signal(str)

    def __init__(self):
        super().__init__()
        print('Inicializando')
        self.camera = None
        self.running = None
        self.video_size = QSize(320, 240)

    def run(self):
        print('Corriendo')
        self.running = True
        self.camera = cv2.VideoCapture(
            0, cv2.CAP_DSHOW)

        if not self.camera.isOpened():
            self.running = False
            self.finished.emit()
            self.onError.emit("No se pudo abrir la cámara")
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT,
                        self.video_size.height())
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0],
                                           QImage.Format.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(
                    self.video_size.width(), self.video_size.height(), Qt.AspectRatioMode.KeepAspectRatio)
                print("it got the pic")
                self.imageUpdate.emit(Pic)

        print("\nfinished signal emited")
        self.finished.emit()
