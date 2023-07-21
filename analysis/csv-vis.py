#!/bin/python3

import matplotlib.pyplot as plt

data_file = "./data/expr3/pipe_rcv.csv"

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
