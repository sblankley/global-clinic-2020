# control.py

from backend import CSVReader, optimization

def run_opt(fileName):
    CSVReader.read(fileName)
    optimization.group()

# settings.init()
# CSVReader.read(fileName)
# taskgrouping.group()
# stationPlacement.run_stationPl()