#!/bin/python3

import matplotlib.pyplot as plt
from utils import *
from config import *
import gc
import itertools

# Do some quick math
link_speed_bps = 9.7 * (1000**3)
sec_per_bit = 1 / link_speed_bps
sec_per_byte = sec_per_bit * (8 / 1) # Covert by mult by bits/byte



def generate_byte_arrivals_array(arrivals, sizes, sec_per_byte):
    byte_arrival_array = []

    for i, arrival_time in enumerate(arrivals):
        byte_arrival_array += [ arrival_time ]
        packet_size = sizes[i]
        # Add entry for each byte that is recieved
        for _ in range(0, packet_size):
            # We could do this at the bit level but idk if necessary
            byte_arrival_array += \
                [ byte_arrival_array[-1] + sec_per_byte ]        

    return byte_arrival_array



def expensive_plot(times, sizes, sec_per_byte):
    x_axis = generate_byte_arrivals_array(times, sizes, sec_per_byte)
    y_axis = [ 1 for x in range(0, len(x_axis)) ]

    plt.scatter(x=x_axis, y=y_axis)
    plt.show()



def generate_packet_start_stop_times(arrivals, sizes, sec_per_byte):
    times = [] # Should be a tuple

    for i, arrival_time in enumerate(arrivals):
        packet_size = sizes[i]
        stop_time = arrival_time - ( packet_size * sec_per_byte )
        times += [ [ arrival_time, stop_time ] ]
    return times


def line_plot(time_tuples):

    ind = 0

    line_colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
    
    for data in time_tuples:
        x1 = data
        y1 = [ind,ind]
        plt.plot(x1, y1, linewidth=5, color=next(line_colors), linestyle='-')
        ind += 1
    plt.title(data_file.split('/')[2])
    plt.show()


"""
To add packet loading dots we need to:
    1) find how long after the current point, the next byte loading
        should be written
        - Find sec / byte
    2) read the length of every read packet
    Loop over size & times and:
        3) Add data point to array for arrival
        4) Add data point for every byte read
    5) plot data array as X values
        - Give y values the value of 1
"""


# expensive_plot(aligned_time[:1000], sizes[:1000], sec_per_byte)
"""
bottom=0

while bottom < len(aligned_time):
    packet_data = generate_packet_start_stop_times\
            (aligned_time[bottom:bottom + 1000], sizes, sec_per_byte)
    line_plot(packet_data)
    bottom += 1000
"""
# new_times, new_sizes = chop_on_time(sizes, aligned_time, 0, 16)
"""
print('step 1')
new_times, new_sizes = chop_on_time(sizes, times, 10, 10.000002)
del times
del sizes

print('step 2')
packet_data = generate_packet_start_stop_times\
        (new_times, new_sizes, sec_per_byte)
del new_times
del new_sizes

print(packet_data)
"""

"""
times, sizes = chop_on_time(sizes, times, 10, 11)

packet_data = generate_packet_start_stop_times\
        (times, sizes, sec_per_byte)

del times
del sizes
gc.collect()

line_plot(packet_data)
"""


arrival_tuples = [] # Should be a tuple
data_loaded = 0


def packet_deliveries(streamer):

    global arrival_tuples # Should be a tuple
    global data_loaded

    # Current index points to location to be inserted
    packet_size, arrival_time = streamer.index(-1) 

    stop_time = arrival_time - ( packet_size * sec_per_byte )
    arrival_tuples += [ [ arrival_time, stop_time ] ]

    data_loaded += 1
    if data_loaded > 100000: 
        streamer.exit = True



def avg_deliveries(streamer):

    global arrival_tuples # Should be a tuple
    global data_loaded

    if streamer.insert_index != 0: return

    # Current index points to location to be inserted
    packet_sum = np.sum(streamer.sizes)

    start_time = streamer.arrivals[-1] - (sec_per_byte * packet_sum)

    stop_time = streamer.arrivals[-1]

    arrival_tuples += [ [ start_time, stop_time ] ]

    data_loaded += 1
    if data_loaded > 100000: 
        streamer.exit = True

"""
window_size = 5
streamer = Streamer(data_file, window_size)

streamer.stream(avg_deliveries, skip = 30000000)

line_plot(arrival_tuples)

x_axis = np.zeros(100000000, dtype=float)
y_axis = np.zeros(100000000, dtype=float)
index = 0
"""

def generate_gap_hist_data(streamer):
    global x_axis
    global y_axis
    global index

    gap = streamer.index(-1)[1] - streamer.index(-2)[1]
    x_axis[index] = streamer.index(-2)[1] + (gap / 2)
    y_axis[index] = gap

    index += 1
    if index > 100000000:
        streamer.exit = True

"""
window_size = 5
streamer = Streamer(data_file, window_size)

plt.figure()

plt.axhline(y= 1.2096 * 10**-6, color='red', linewidth=0.5)

streamer.stream(generate_gap_hist_data, skip = 30000000)
plt.scatter(x=x_axis, y=y_axis) #, s=0.5)

plt.show()
"""

times = [] # Should be a tuple

# def stream_start_stop_times(arrivals, sizes, sec_per_byte):
def stream_start_stop_times(streamer):
    global times # Should be a tuple

    if len(times) and 0.005 + times[-1][0] < streamer.arrivals[streamer.insert_index]:
        print('num in group: ', streamer.group)
        streamer.group = 0
    else:
        streamer.group += 1

    sec_per_bit = 1 / (100000000)

    arrival_time = streamer.arrivals[streamer.insert_index]
    packet_size = 8 * streamer.sizes[streamer.insert_index]
    stop_time = arrival_time - ( (packet_size) * sec_per_bit )
    times += [ [ arrival_time, stop_time ] ]

    if streamer.insert_index == streamer.buffer_size - 1: 
        streamer.exit = True




window_size = 100000
streamer = Streamer(data_file, window_size)

streamer.group = 0

streamer.stream(stream_start_stop_times, skip=300000, align=True)
# sizes, times = load_erik_data(data_file)

# packet_times = generate_packet_start_stop_times\
#         (times, sizes, (8 / (100 * 1024 * 1024)))

line_plot(times)

