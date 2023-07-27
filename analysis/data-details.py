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
        arrivals += [ float(arrvial) ]
    return sizes, arrivals

def load_data(filename):
    fd = open(filename)
    lines = fd.read()
    data_tuples = lines.split(',')
    arrivals = []
    for x in data_tuples:
        if not x: continue
        arrivals += [ float(x.split(':')[1]) ]
    return arrivals

def align_time_data(time_data):
    shift = float(time_data[0])
    shifted_data = [ float(x) - shift for x in time_data ]
    return shifted_data
    
arrival_times = load_data('./data/01/pipe_rcv.csv')
print(len(arrival_times))
for el in align_time_data(arrival_times): 
    print(el)

