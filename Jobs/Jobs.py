from PySide6.QtCore import Signal, QObject
from modules.wifi import connect, createNewConnection
from modules.constants import config
from time import sleep
from modules.helpers import is_admin
from function import sync_date_time
from modules.backend_connection import get_config
import asyncio

class Jobs(QObject):
    finished = Signal()
    progress = Signal(int)
    configData = Signal(dict)
    online = False

    def run(self):
        """Long-running task."""
        self.online = self.check_online()
        
        if self.online == False:
            createNewConnection(
                config['WIFI']['SSID'], config['WIFI']['SSID'], config['WIFI']['PASS'])
            createNewConnection(
                config['WIFI']['SSID5G'], config['WIFI']['SSID5G'], config['WIFI']['PASS5G'])
            connect(config['WIFI']['SSID'], config['WIFI']['SSID'])
            connect(config['WIFI']['SSID5G'], config['WIFI']['SSID5G'])
            sleep(1)
        self.online = self.check_online()
        if is_admin() and self.online:
            
            sync_date_time()
            
        self.configData.emit(asyncio.run(get_config()))
        self.finished.emit()

    def check_online(self):
        return (lambda a: 'Success' if 0 == a.system('ping finxter.com -w 4') else 'Failure')(__import__('os'))