#!/bin/python3

import matplotlib.pyplot as plt

# data_file = "./data/exp1/pipe-data.csv"
data_file = "./data/baseline/baseline-2.csv"
# data_file = "./data/exp2/exp2.csv"

fd = open(data_file)

text = fd.read()

data_tuples_text = text.split(',')

data_points_full = []
x = []
y = []

for point in data_tuples_text:
    if point:
        [length, time] = point.split(':')
        data_points_full += [ [int(length), float(time)] ]
        x += [ float(time) * 10**15  ]
        y += [ len(y) + 1 ]
        # y += [ 1 ]


plt.scatter(x=x, y=y)
plt.show()
