import subprocess
import enum
import re
import json
import sys
from os import path, getenv

from ..constants import dirname, programs_path


class ReadMode(enum.Enum):
    start = 1
    controllermap = 2
    disklist = 3
    drivedata = 4
    smartdata = 5
    identifydata = 6
    smartreaddata = 7
    smartreadthreshold = 8


# generate data
# print("Running DiskInfo.exe")
def DiskInfo():
    print('Obteniendo info de los discos')
    if not getattr(sys, 'frozen', False):
        command = "diskinfo/DiskInfo.exe"
        diskinfo_file = "diskinfo/DiskInfo.txt"
    else:
        command = 'DiskInfo.exe'
        diskinfo_file = "DiskInfo.txt"
    try:
        print(f'"{path.join(programs_path, command)}" /CopyExit')
        status = subprocess.call(f'"{path.join(programs_path, command)}" /CopyExit')
    except WindowsError as e:
        if "Error 740" in str(e):
            print(
                "This application must be run as an administrator to get raw access to drives.")
            print("Exiting.")
        else:
            raise e

    if status != 0:
        raise Exception("DiskInfo.exe exited with status code "+status)

    # read data
    input_data = None

    with open(path.join(programs_path, diskinfo_file), 'r', encoding='utf-8') as f:
        input_data = f.read()

    # parse data
    obj = []
    curmode = ReadMode.start
    curdiskname = None
    curdiskidx = None
    curcontroller = None

    for linenum, line in enumerate(input_data.splitlines()):

        # skip blank lines
        if len(line) == 0:
            # print("blank", line)
            continue

        # mode pivots
        if re.search("^-- Controller Map", line):
            curmode = ReadMode.controllermap
            continue

        if re.search("^-- Disk List", line):
            curmode = ReadMode.disklist
            continue

        if re.search("^-- S.M.A.R.T. ", line):
            curmode = ReadMode.smartdata
            continue

        # if re.search("^-- IDENTIFY_DEVICE ", line):
        #     curmode = ReadMode.identifydata
        #     continue

        if re.search("^-- SMART_READ_DATA ", line):
            curmode = ReadMode.smartreaddata
            continue

        if re.search("^-- SMART_READ_THRESHOLD ", line):
            curmode = ReadMode.smartreadthreshold
            continue

        # if curmode == ReadMode.controllermap:
        #     if line.startswith(" + "):
        #         curcontroller = line[len(" + "):]
        #         obj["controllers_disks"][curcontroller] = []
        #     if line.startswith("   - "):
        #         obj["controllers_disks"][curcontroller].append(
        #             line[len("   - "):])
        #     continue

        if curmode == ReadMode.disklist:
            result = re.search("^ \((\d+)\) (.*) : (.*) \[.*$", line)
            if result:
                idx, name, size = result.groups()
                obj.append(
                    {"DiskNum": idx, "Model": name, "Disk Size": size})
            elif line.startswith("-----------------"):
                curmode = ReadMode.drivedata
            continue

        result = re.search("^ \((\d+)\) (.*)$", line)
        if result:
            curmode = ReadMode.drivedata
            curdiskidx, curdiskname = result.groups()
            continue

        if curmode == ReadMode.drivedata:
            splitstrip = [x.strip() for x in line.split(" : ")]
            if len(splitstrip) > 1:
                attribute, value = splitstrip
                obj[int(curdiskidx)-1][attribute] = value
            continue

        # if curmode == ReadMode.smartdata:
        #     result = re.search(
        #         "^([A-F0-9]{2}) _*(\d*) _*(\d*) _*(\d*) ([A-F0-9]{12}) (.*)$", line)
        #     if result:
        #         _id, cur, wor, thr, rawvalues, attributename = result.groups()
        #         smartobj = {"ID": _id, "Cur": cur, "Wor": wor, "Thr": thr,
        #                     "RawValues": rawvalues, "Attribute Name": attributename}

        #         if "S.M.A.R.T." not in obj[int(curdiskidx)-1]:
        #             obj[int(curdiskidx)-1]["S.M.A.R.T."] = []

        #         obj[int(curdiskidx)-1]["S.M.A.R.T."].append(smartobj)
        #     continue

        # if curmode == ReadMode.identifydata:
        #     # skip header
        #     if line.startswith("    "):
        #         continue

        #     # extract hex, stripping off index at beginning
        #     hexdata = "".join(line.split(" ")[1:])

        #     # initialize on disk object if needed
        #     if "IDENTIFY_DEVICE" not in obj[int(curdiskidx)-1]:
        #         obj[int(curdiskidx)-1]["IDENTIFY_DEVICE"] = ""

        #     obj[int(curdiskidx)-1]["IDENTIFY_DEVICE"] += hexdata
        #     continue

        # if curmode == ReadMode.smartreaddata:
        #     # skip header
        #     if line.startswith("    "):
        #         continue

        #     # extract hex, stripping off index at beginning
        #     hexdata = "".join(line.split(" ")[1:])

        #     # initialize on disk object if needed
        #     if "SMART_READ_DATA" not in obj[int(curdiskidx)-1]:
        #         obj[int(curdiskidx)-1]["SMART_READ_DATA"] = ""

        #     obj[int(curdiskidx)-1]["SMART_READ_DATA"] += hexdata
        #     continue

        # if curmode == ReadMode.smartreadthreshold:
        #     # skip header
        #     if line.startswith("    "):
        #         continue

        #     # extract hex, stripping off index at beginning
        #     hexdata = "".join(line.split(" ")[1:])

        #     # initialize on disk object if needed
        #     if "SMART_READ_THRESHOLD" not in obj[int(curdiskidx)-1]:
        #         obj[int(curdiskidx)-1]["SMART_READ_THRESHOLD"] = ""

        #     obj[int(curdiskidx)-1]["SMART_READ_THRESHOLD"] += hexdata
        #     continue

    return obj
    # output data
    # with open(path.join(dirname,"programs/CrystalDiskInfo/DiskInfoParser.json"),"w") as f:
    #   f.write(json.dumps(obj, indent=2, separators=(",", ": "), sort_keys=True))
