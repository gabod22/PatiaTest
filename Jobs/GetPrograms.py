# MenuBar
from PySide6.QtCore import Signal, QObject
from modules.helpers.system_accions import get_all_programs
from modules.constants import dirname
import os
class GetProgramsJob(QObject):
    
    finished = Signal(list)
    progress = Signal(str)
    
    def run(self):
        
        self.progress.emit('Obteniendo los programas')

        programs = get_all_programs(os.path.join(dirname, 'programs'))
        self.finished.emit(programs)
        # self.finished.emit()
        # pixmap = QPixmap(program['icon'])
        # icon = QIcon(pixmap)
        