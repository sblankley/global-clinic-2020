# control.py

import CSVReader, taskgrouping 

def run_opt(fileName):
    CSVReader.read(fileName)
    taskgrouping.group()
