# -*- coding: latin-1 -*-
import os
from modules.iconExtractor import extract_icon, IconSize
from modules.helpers.converters import win32_icon_to_image
from modules.constants import dirname


def filter_exe_files(file):
    if file.find('.exe') > 0:
        return True
    return False


def get_all_programs():
    entries = os.listdir(os.path.join(dirname, 'programs'))
    # print(entries)
    programs = list(filter(filter_exe_files, entries))
    program_list = list()
    for program in programs:
        p = dict()
        # print(os.path.join(
        #     dirname, 'programs') + "/" + program)
        # icon = extract_icon(os.path.join(
        #     dirname, 'programs') + "/" + program, IconSize.LARGE)

        # img = win32_icon_to_image(icon, IconSize.LARGE)
        p["name"] = program
        p["icon"] = None

        program_list.append(p)

    return program_list
