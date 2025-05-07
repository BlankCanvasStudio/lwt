#!/bin/python3

import matplotlib.pyplot as plt

# Read the file and extract the x and y values
x_values = []
y_values = []
x = 1
with open('importance-feats.txt', 'r') as file:
    for line in file:
        y = float(line.strip())
        y_values.append(y)
        x_values.append(x)
        x += 1

# Plot the values
plt.bar(x_values, y_values)
plt.xlabel('Feature Number')
plt.ylabel('Importance Score')
plt.title('Plot of Feature Importance')
plt.show()


