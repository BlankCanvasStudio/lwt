#!/bin/python3

def load_full_data(filename):
    fd = open(filename)
    lines = fd.read()
    data_tuples = lines.split(',')
    sizes = []
    arrivals = []
    for x in data_tuples:
        if not x: continue
        [ size, arrival ] = x.split(':')
        sizes += [ int(size) ]
        arrivals += [ float(arrival) ]
    return sizes, arrivals

sizes, arrivales = load_full_data('./data/expr20/pipe_rcv.csv')

gaps = {}

for i in range(0, len(arrivales) -2):
    gap = arrivales[i+1] - arrivales[i]
    if gap not in gaps:
        gaps[gap] = 1
    else:
        gaps[gap] += 1

for key, value in sorted(gaps.items()):
    print(key, ':', value)

