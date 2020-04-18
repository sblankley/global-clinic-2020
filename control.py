# control.py

import CSVReader, taskgrouping, stationPlacement

def run_opt(fileName):
    CSVReader.read(fileName)
    taskgrouping.group()
    stationPlacement.run_stationPl()