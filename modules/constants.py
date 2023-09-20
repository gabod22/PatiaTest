# -*- coding: latin-1 -*-
from os import path
from .files_managment import read_yaml
dirname = path.join(path.dirname(__file__), '..')
print(dirname)

gspread_file = path.join(dirname, 'config_files/gspread_config.json')

config_file = path.join(dirname, "config_files\config.yaml")

power_scheme_path = path.join(dirname, "config_files\planpruebas.pow")

config_path = path.join(dirname, "config_files")

config = read_yaml(config_file)
