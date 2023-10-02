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

import pickle
from os import path

from modules.systeminfo import get_system_info
from modules.helpers import isConnected


class Jobs(QObject):
    finished = Signal()
    progress = Signal(str)
    configData = Signal(dict)
    systemData = Signal(dict)
    error = Signal(str)
    online = False
    config = None

    def run(self):
        """Long-running task."""
        self.config = read_yaml(config_file)
        self.progress.emit('Comprobando conexion a internet.')
        self.online = isConnected()

        if self.online == False:
            self.progress.emit('No hay conexión a internet.')
            createNewConnection(
                self.config['WIFI']['SSID'], self.config['WIFI']['SSID'], self.config['WIFI']['PASS'])
            createNewConnection(
                self.config['WIFI']['SSID5G'], self.config['WIFI']['SSID5G'], self.config['WIFI']['PASS5G'])
            self.progress.emit('Contectando a internet')
            connect(self.config['WIFI']['SSID'], self.config['WIFI']['SSID'])
            connect(self.config['WIFI']['SSID5G'], self.config['WIFI']['SSID5G'])
            sleep(2)
        self.online = isConnected()
        if self.online:
            self.progress.emit('Internet conectado.')
            self.progress.emit('Obteniendo configuración del servidor.')
            try:
                config = asyncio.run(get_config())
                self.configData.emit(config)
                self.progress.emit('Configuración obtenida.')
            except Exception as e:
                print("Error al obtener la configuración: ", e)
                self.progress.emit(e)
            
            self.progress.emit('Guardando configuración')
            with open(path.join(dirname, "config_files\config.pkl"), 'wb') as f:
                pickle.dump(config, f)

        else:
            self.progress.emit('No hay internet, obteniendo configuración guardada.')
            try:
                with open(path.join(dirname, "config_files\config.pkl"), 'rb') as f:
                    config = pickle.load(f)
                    self.configData.emit(config)
            except Exception as e:
                self.error.emit('No hay coneccion a internet y no se pudo cargar la información.')
                print(e)
            self.error.emit('No hay coneccion a internet, revise la conexión. Se cargó la información de respaldo.')

        if is_admin() and self.online:
            self.progress.emit('Sincronizando la hora')
            sync_date_time()
        

        self.finished.emit()



    