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
        sizes += [ size ]
        arrivals += [ arrvial ]
    return sizes, arrivals

def load_data(filename):
    fd = open(filename)
    lines = fd.read()
    data_tuples = lines.split(',')
    arrivals = []
    for x in data_tuples:
        if not x: continue
        arrivals += [ x.split(':')[1] ]
    return arrivals

arrival_times = load_data('./data/expr4/pipe_rcv.csv')
print(len(arrival_times))
