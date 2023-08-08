# -*- coding: latin-1 -*-

import yaml
import json



def read_json_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def write_json_file(file_path, data):
    with open(file_path, 'w') as outfile:
        outfile.write(data)

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def write_yaml(file_path, data):
    with open(file_path, "w") as file:
        yaml.dump(data, file)