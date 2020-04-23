# control.py

from backend import CSVReader, taskgrouping

def run_opt(fileName):
    CSVReader.read(fileName)
    taskgrouping.group()

# settings.init()
# CSVReader.read(fileName)
# taskgrouping.group()
# stationPlacement.run_stationPl()
