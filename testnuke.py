opList = [[0.0], [1.0], [1.0], [0.0], [2.0], [0.0]]

workers_assigned = []

for index in range(0,len(opList)):
    for sub_val in range(0,len(opList[index])):
        workers_assigned.append(str(opList[index][sub_val]))

print(workers_assigned)