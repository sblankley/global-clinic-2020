# control.py

from backend import settings, CSVReader, taskgrouping, stationPlacement

def run_opt(fileName):
    CSVReader.read(fileName)
    taskgrouping.group()
    stationPlacement.run_stationPl()

# settings.init()
# CSVReader.read(fileName)
# taskgrouping.group()
# stationPlacement.run_stationPl()