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

sizes, arrivales = load_full_data('./data/expr24/pipe_rcv.csv')

gaps_list = []
gaps = {}

for i in range(0, len(arrivales) -2):
    gap = arrivales[i+1] - arrivales[i]
    if gap not in gaps:
        gaps[gap] = 1
    else:
        gaps[gap] += 1
    gaps_list += [ gap ]

for key, value in sorted(gaps.items()):
    print(key, ':', value)

sorted_list = sorted(gaps.keys())

top_sorted = sorted_list[(len(sorted_list) - 30):]

for ind in top_sorted:
    # print('delay:', ind)
    print('index: ', gaps_list.index(ind))
    # print('')

