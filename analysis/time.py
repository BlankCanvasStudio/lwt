#!/bin/python3

import matplotlib.pyplot as plt

from config import *
import utils

def calc_dead_time(streamer):
    if streamer.insert_index != streamer.buffer_size - 1: return

    sorted_indicies = np.argsort(streamer.arrivals)
    streamer.sizes = streamer.sizes[sorted_indicies]
    streamer.arrivals = streamer.arrivals[sorted_indicies]

    for i in range(0, streamer.buffer_size-1):
        time1 = streamer.arrivals[i]
        time2 = streamer.arrivals[i+1]
        size2 = streamer.sizes[i+1]
        
        # print(time1, time2, size2)
        # gap = (time2 - time1) - packet_delivery_time
        gap = (time2 - time1) - ((8 * size2) / streamer.link_bps)

        if gap > 0:
            streamer.output += gap
        else:
            streamer.neg_time += gap

   
window_size = 100000
bps = 97 * 1000 * 1000
# streamer = utils.ErikStreamer(data_file, buffer_size = window_size, link_bps = bps, output = 0)
streamer = utils.Streamer(data_file, buffer_size = window_size, link_bps = bps, output = 0)
streamer.neg_time = 0
streamer.stream(calc_dead_time, skip=50000)

print("dead time:", streamer.output)
print("negative gaps:", streamer.neg_time)

