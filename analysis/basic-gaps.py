#!/bin/python3

import matplotlib.pyplot as plt

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


def align_time_data(time_data):
    shift = float(time_data[0])
    shifted_data = [ float(x) - shift for x in time_data ] 
    return shifted_data
 

sizes, arrivales = load_full_data('./data/01/pipe_rcv.csv')

gaps_list = []
gaps = {}

for i in range(0, len(arrivales) -2):
    gap = arrivales[i+1] - arrivales[i]
    if gap not in gaps:
        gaps[gap] = 1
    else:
        gaps[gap] += 1
    gaps_list += [ gap ]

"""
for key, value in sorted(gaps.items()):
    print(key, ':', value)
"""

sorted_list = sorted(gaps.keys())

top_sorted = sorted_list[(len(sorted_list) - 30):]

aligned_time = align_time_data(arrivales)

min_delay = 7
max_delay = 9
indexes_in_range = [ index for index, value in enumerate(aligned_time) if min_delay <= value <= max_delay ]

for ind in indexes_in_range:
    # if gaps_list[ind] < 0.00011 or gaps_list[ind] > 0.00013:
    if gaps_list[ind] > 0.00015:
        print('delay:', gaps_list[ind])
        print('time: ',aligned_time[ind])
        print('')

