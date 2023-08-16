from PySide6.QtCore import Signal, QObject
from modules.wifi import connect, createNewConnection
from modules.constants import config
from time import sleep
from modules.helpers import is_admin
from function import sync_date_time

class Jobs(QObject):
    finished = Signal()
    progress = Signal(int)
    batteryInfo = Signal(list)
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
        self.finished.emit()

    def check_online(self):
        return (lambda a: True if 0 == a.system('ping google.com -w 4 > clear') else False)(__import__('os'))