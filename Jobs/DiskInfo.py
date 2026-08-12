# MenuBar
from PySide6.QtCore import Signal, QObject

from modules.parsers.DiskInfoParser import DiskInfo

class DiskInfoJob(QObject):
    
    finished = Signal(object)
    progress = Signal(object)
    
    def run(self):

        self.progress.emit('Obteniendo info de las unidades de almacenamiento')
        try:
            disks = DiskInfo()
            print(disks)
        except Exception as e:
            disks = {}
            print(e)
        finally:
            self.finished.emit(disks)
        