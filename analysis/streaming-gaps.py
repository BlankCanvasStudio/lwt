#!/bin/python3

from config import *
import utils 
import numpy as np
import matplotlib.pyplot as plt

link_speed = 100 * (1000 * 1000 * 1000)


def check_gaps(streamer_in):
    total_packet_size = np.sum(streamer_in.sizes) * 8
    expected_time = total_packet_size / link_speed
    
    # Last inserted index is the current insert_index
    if streamer_in.insert_index:
        most_recent_insert = streamer_in.insert_index - 1
    else:
        most_recent_insert = streamer_in.buffer_size - 1

    time_taken = streamer_in.arrivals[most_recent_insert] - streamer_in.arrivals[streamer_in.insert_index]

    if time_taken > expected_time:
        print("Delta: ", time_taken - expected_time)


# streamer = utils.Streamer(data_file, check_gaps, buffer_size = 10)
# streamer.stream()

gbps_to_time = {}
gbps_count = {}
odd_gbps = {}
ping_gbps = {}
ping_times = []

def count_window_times(streamer_in):
    global ping_times
    if streamer_in.insert_index != 0: return

    odd = False
    ping_occured = False


    # Additional code to remove packets for detection purposes
    if len(np.where(streamer_in.sizes != 1476)[0]):
        odd = True

    indicies = np.where(streamer_in.sizes == 1500)[0]

    if len(indicies):
        ping_occured = True

    new_sizes = streamer_in.sizes
    new_arrivals = streamer_in.arrivals

    for i, el in enumerate(indicies):
        new_sizes = np.delete(new_sizes, el - i)
        new_arrivals = np.delete(new_arrivals, el - i)
        size, arrival = streamer_in.read()
        while size == 1500:
            size, arrival = streamer_in.read()
        new_sizes = np.append(new_sizes, size)
        new_arrivals = np.append(new_arrivals, arrival)


    streamer_in.sizes = new_sizes
    streamer_in.arrivals = new_arrivals


    tot_size = np.sum(streamer_in.sizes)
    bps = tot_size / (streamer_in.arrivals[-1] - streamer_in.arrivals[0])
    gbps = (8*bps) / (1000*1000*1000)
    

    if ping_occured:
        ping_times += [ np.average(streamer_in.arrivals) ]
        if gbps not in ping_gbps: 
            ping_gbps[gbps] = 1
        else: 
            ping_gbps[gbps] += 1

    if gbps not in gbps_count: 
        gbps_count[gbps] = 1
        gbps_to_time[gbps] = [ np.average(streamer_in.arrivals) ]
    else: 
        gbps_count[gbps] += 1
        if len(gbps_to_time[gbps]) < 10:
            gbps_to_time[gbps] += [ np.average(streamer_in.arrivals) ]

    if odd:
        if gbps not in odd_gbps: odd_gbps[gbps] = 1
        else: odd_gbps[gbps] += 1


window_size = 5
streamer = utils.Streamer(data_file, window_size)
# streamer.stream(count_window_times)
streamer.stream(count_window_times)

"""
print("gbps count:")
print(gbps_count)
print('\n\n')

print('odd gbps:')
print(odd_gbps)
print('\n\n')

print('ping gbps:')
print(ping_gbps)
print('\n\n')

print('possible detections: ')
for key, value in gbps_count.items():
    if value < 10:
        print(key)

print('odd detections: ')
for key, value in odd_gbps.items():
    if value < 10:
        print(key)

print('ping detections: ')
for key, value in ping_gbps.items():
    if value < 10:
        print(key)
"""

"""
low_end_detection = []

for key, value in gbps_count.items():
    if value < 10:
        low_end_detection += [ key ]

plt.title(data_file.split('/', 2)[2] + ' window: ' + str(window_size))
plt.scatter(x=gbps_count.keys(), y= [ 0 for x in gbps_count.keys() ]) #, s=0.5)
plt.scatter(x=odd_gbps.keys(), y= [ 0.1 for x in odd_gbps.keys() ], color='red')
plt.scatter(x=ping_gbps.keys(), y= [ 0.2 for x in ping_gbps.keys() ], color='lime')
plt.scatter(x=low_end_detection, y= [ 0.3 for x in low_end_detection ], color='lime')
"""

low_end_detection = []

for key, value in gbps_count.items():
    if value < 10 and key > 3:
    # if value < 10:
        low_end_detection += gbps_to_time[key]

plt.scatter(x=low_end_detection, y= [ 0 for x in low_end_detection ]) #, s=0.5)
plt.scatter(x=ping_times, y= [ 0 for x in ping_times ], color='lime', s=0.75)

plt.show()

