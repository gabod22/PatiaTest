# MenuBar
from PySide6.QtCore import Signal, QObject
from modules.programs import get_all_programs

from modules.parsers.GpuzParser import get_gpuz_info

class GpuzJob(QObject):
    
    finished = Signal(list)
    progress = Signal(str)
    
    def run(self):

        self.progress.emit('Obteniendo info de las GPUs')

        try:
            gpus = get_gpuz_info()
        except Exception as e:
            print(e)
            gpus = []
        finally:
            self.finished.emit(gpus)
    
        