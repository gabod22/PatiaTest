from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QMessageBox
from modules.wifi import connect, createNewConnection
from time import sleep
from modules.helpers import is_admin
from function import sync_date_time
from modules.backend_connection import get_config, get_computer
from modules.files_managment import read_yaml
from modules.constants import dirname, config_file
import asyncio

import pickle
import json
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
    system = None
    showDialog = Signal()
    thisComputer = Signal(dict)

    def run(self):
        """Long-running task."""
        self.config = read_yaml(config_file)
        self.progress.emit('Comprobando conexion a internet.')
        self.online = isConnected()

        self.system = get_system_info(
            progress_callback=self.progress, on_error=self.error, show_dialog=None)

        self.systemData.emit(self.system)
        print(self.system)
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
        if self.online:
            self.progress.emit('Internet conectado.')
            self.progress.emit('Obteniendo configuración del servidor.')
            try:
                config = asyncio.run(get_config())
                if config == None:
                    print('No se pudo obtener la configuración')
                    raise Exception('No se obtuvo la configuración')
                else:
                    self.configData.emit(config)
                    # print(config)
                    self.progress.emit('Configuración obtenida.')
                    self.progress.emit('Guardando configuración')
                    with open(path.join(dirname, "config_files\config.pkl"), 'wb') as f:
                        pickle.dump(config, f)
            except Exception as e:
                print("Error al obtener la configuración: ", e)
                self.progress.emit(e)
                self.get_offline_config()

            self.progress.emit('Obteniendo registro de la computadora')
            try:
                (response, r) = asyncio.run(get_computer(
                    serial_number=self.system["bios"]["SerialNumber"]))

                if response.status != 404:
                    r = json.loads(r)
                    self.thisComputer.emit(r['data'])
                    self.progress.emit('La computadora ya está registrada')
                    self.enable_register = True
                else:
                    self.progress.emit('No hay registro de la computadora')
                    self.showDialog.emit()
            except (TypeError, AttributeError) as e:
                print(e)
                self.progress.emit(
                    'No hay conexion con el servidor, se deshabilitará la opcion de reporte')

        else:
            self.progress.emit(
                'No hay internet, obteniendo configuración guardada.')
            self.get_offline_config()

        if is_admin() and self.online:
            self.progress.emit('Sincronizando la hora')
            sync_date_time()

        self.finished.emit()

    def get_offline_config(self):
        try:
            with open(path.join(dirname, "config_files\config.pkl"), 'rb') as f:
                config = pickle.load(f)
                self.configData.emit(config)
                print('Cargando desde el archivo')
                # print(config)
        except Exception as e:
            self.error.emit(
                'No hay coneccion a internet y no se pudo cargar la información.')
            print(e)
        self.error.emit(
            'No hay coneccion a internet, revise la conexión. Se cargó la información de respaldo.')
