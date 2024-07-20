from PySide6.QtCore import Signal, QObject
from modules.wifi import connect, createNewConnection
from time import sleep
from modules.helpers import is_admin
from function import sync_date_time
from modules.files_managment import read_yaml
from modules.constants import dirname, config_file


from modules.systeminfo import get_system_info
from modules.helpers import isConnected


class Initialization(QObject):
    finished = Signal()
    progress = Signal(str)
    systemData = Signal(dict)
    error = Signal(str)
    online = False
    config = None
    system = None
    showDialog = Signal()

    def run(self):
        """Long-running task."""
        self.config = read_yaml(config_file)
        self.progress.emit('Comprobando conexion a internet.')
        self.online = isConnected()

        self.system = get_system_info(
            progress_callback=self.progress, on_error=self.error, show_dialog=None)

        self.systemData.emit(self.system)

        if self.online == False:
            self.progress.emit('No hay conexión a internet.')
            createNewConnection(
                self.config['WIFI']['SSID'], self.config['WIFI']['SSID'], self.config['WIFI']['PASS'])
            createNewConnection(
                self.config['WIFI']['SSID5G'], self.config['WIFI']['SSID5G'], self.config['WIFI']['PASS5G'])
            self.progress.emit('Contectando a internet')
            connect(self.config['WIFI']['SSID'], self.config['WIFI']['SSID'])
            connect(self.config['WIFI']['SSID5G'],
                    self.config['WIFI']['SSID5G'])
            sleep(2)
        self.online = isConnected()
            
        if is_admin() and self.online:
            self.progress.emit('Sincronizando la hora')
            sync_date_time()

        self.finished.emit()

