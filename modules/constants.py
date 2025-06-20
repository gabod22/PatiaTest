# -*- coding: UTF-8 -*-
from os import path
import sys
from .files_managment import read_yaml

if getattr(sys, 'frozen', False):
    dirname = path.join(path.dirname(sys.executable), '_internal')
elif __file__:
    dirname = path.join(path.dirname(__file__), '..')

programs_path = path.join(dirname, 'programs')

config_file = path.join(dirname, 'config_files\config.yaml')

power_scheme_path = path.join(dirname, 'config_files\planpruebas.pow')

config_path = path.join(dirname, 'config_files')

config = read_yaml(config_file)
