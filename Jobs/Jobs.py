from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QMessageBox
from modules.wifi import connect, createNewConnection
from time import sleep
from modules.helpers import is_admin
from function import sync_date_time
from modules.backend_connection import get_config
from modules.files_managment import read_yaml
from modules.constants import dirname, config_file
import asyncio
import socket
import pickle
from os import path


class Jobs(QObject):
    finished = Signal()
    progress = Signal(int)
    configData = Signal(dict)
    online = False
    error = Signal(str)
    config = None

    def run(self):
        """Long-running task."""
        self.config = read_yaml(config_file)
        self.online = self.isConnected()

        if self.online == False:
            createNewConnection(
                self.config['WIFI']['SSID'], self.config['WIFI']['SSID'], self.config['WIFI']['PASS'])
            createNewConnection(
                self.config['WIFI']['SSID5G'], self.config['WIFI']['SSID5G'], self.config['WIFI']['PASS5G'])
            connect(self.config['WIFI']['SSID'], self.config['WIFI']['SSID'])
            connect(self.config['WIFI']['SSID5G'], self.config['WIFI']['SSID5G'])
            sleep(2)
        self.online = self.isConnected()
        if self.online:
            config = asyncio.run(get_config())
            self.configData.emit(config)
            print(config)

            with open(path.join(dirname, "config_files\config.pkl"), 'wb') as f:
                pickle.dump(config, f)

        else:
            try:
                with open(path.join(dirname, "config_files\config.pkl"), 'rb') as f:
                    config = pickle.load(f)
                    self.configData.emit(config)
                    print("imprimiendo configuracion",config)
            except Exception as e:
                self.error.emit('No hay coneccion a internet y no se pudo cargar la información')
                print(e)
            self.error.emit('No hay coneccion a internet, revise la conexión. Se cargó la información de respaldo')

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
