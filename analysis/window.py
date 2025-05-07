#!/bin/python3
import numpy as np
import struct
import binascii
import sys, os

import utils

import matplotlib.pyplot as plt


def analyze_bin_data(filename, avg_size = 100000):

    times = []
    odd_indexes = []
    ping_packets = []
    missed_pings = []

    arrivals = np.zeros(avg_size, dtype='d')
    sizes = np.zeros(avg_size, dtype=int)

    insert_index = 0

    file_size = os.path.getsize(filename)

    with open(filename, 'rb') as fd:
        fd.seek(0)
        fd.read(4)
        offset = struct.unpack('d', fd.read(8))[0]


    with open(filename, 'rb') as fd:

        fd.seek(0)

        while fd.tell() < file_size:
            # This reading method is correct
            sizes[insert_index] = int.from_bytes(fd.read(4), sys.byteorder)
            arrivals[insert_index] = struct.unpack('d', fd.read(8))[0]

            insert_index = (insert_index + 1) % avg_size

            if insert_index == 0:
                tot_size = np.sum(sizes)

                if tot_size != avg_size * 1476: 
                    if 1500 in sizes:
                        ping_packets += [ len(times) ]
                    else:
                        odd_indexes += [ len(times) ]

                if 1500 in sizes and len(times) not in ping_packets:
                    missed_pings += [ len(times) ]

                times += [ arrivals[-1] - offset ]

    return times, odd_indexes, ping_packets, missed_pings


times = []
ping_packets = []
odd_indexes = []
missed_pings = []

def streamer_window_analysis(streamer_in):

    global times
    global ping_packets
    global odd_indexes
    global missed_pings

    if streamer_in.insert_index != 0: return

    tot_size = np.sum(streamer_in.sizes)

    if tot_size != streamer_in.buffer_size * 1476: 
        if 1500 in streamer_in.sizes:
            ping_packets += [ len(times) ]
        else:
            odd_indexes += [ len(times) ]

    if 1500 in streamer_in.sizes and len(times) not in ping_packets:
        missed_pings += [ len(times) ]

    times += [ np.average(streamer_in.arrivals) ]



data_file = "../data-lwt/2s-ping-02/pipe_rcv.csv" 

window_size = 5
# gbps, times, odd_indexes, ping_packets, missed_pings = analyze_bin_data(data_file, avg_size=window_size)

streamer = utils.Streamer(data_file, buffer_size = window_size)
streamer.stream(streamer_window_analysis)


x_axis = times
y_axis = np.zeros(len(times))

odd_times = [ times[x] for x in odd_indexes ]
odd_gbps = np.zeros(len(odd_indexes))

ping_times = [ times[x] for x in ping_packets ]
ping_gbps = np.zeros(len(ping_packets))

missed_times = [ times[x] for x in missed_pings ]
missed_gbps = np.zeros(len(missed_pings))


plt.title(data_file.split('/', 2)[2] + ' window: ' + str(window_size))
plt.scatter(x=x_axis, y=y_axis) #, s=0.5)
plt.scatter(x=odd_times, y=odd_gbps, color='red')
plt.scatter(x=ping_times, y=ping_gbps, color='lime')
plt.scatter(x=missed_times, y=missed_gbps, color='fuchsia')


plt.show()

