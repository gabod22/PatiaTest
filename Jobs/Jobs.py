from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QMessageBox
from modules.wifi import connect, createNewConnection
from modules.constants import config
from time import sleep
from modules.helpers import is_admin
from function import sync_date_time
from modules.backend_connection import get_config
import asyncio
import socket

class Jobs(QObject):
    finished = Signal()
    progress = Signal(int)
    configData = Signal(dict)
    online = False
    error = Signal()

    def run(self):
        """Long-running task."""
        self.online = self.isConnected()
        
        if self.online == False:
            createNewConnection(
                config['WIFI']['SSID'], config['WIFI']['SSID'], config['WIFI']['PASS'])
            createNewConnection(
                config['WIFI']['SSID5G'], config['WIFI']['SSID5G'], config['WIFI']['PASS5G'])
            connect(config['WIFI']['SSID'], config['WIFI']['SSID'])
            connect(config['WIFI']['SSID5G'], config['WIFI']['SSID5G'])
            sleep(2)
        self.online = self.isConnected()
        if self.online:
            self.configData.emit(asyncio.run(get_config()))
        else:
            self.error.emit()
            
        
        if is_admin() and self.online:
            print('Está en linea C:')
            sync_date_time()
        
        
            
        self.finished.emit()



    def isConnected(self):
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            sock = socket.create_connection(("www.google.com", 80))
            if sock is not None:
                print('Clossing socket')
                sock.close
            return True
        except OSError:
            pass
        return False
    
    def showSuccessDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle('Todo correcto')
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def showFailDialog(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle('Error')
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')