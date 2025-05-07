#!/bin/python3

data = open('./data/gap_counts.csv', 'r').read()
arr = data.split(',')

index = 0
with open('./data/gap_counts-2.csv', 'w') as fd:
    while index < len(arr):
        fd.write(arr[index] + ',' + arr[index + 1] + '\n')
        index += 2

