# MenuBar
from PySide6.QtCore import Signal, QObject
from modules.programs import get_all_programs

class GetProgramsJob(QObject):
    
    finished = Signal(list)
    progress = Signal(str)
    
    def run(self):
        
        self.progress.emit('Obteniendo los programas')

        programs = get_all_programs()
        self.finished.emit(programs)
        # self.finished.emit()
        # pixmap = QPixmap(program['icon'])
        # icon = QIcon(pixmap)
        