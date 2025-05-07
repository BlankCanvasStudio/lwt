#!/bin/python3

from utils import *
from config import *


def queuing_info(streamer):
    if streamer.insert_index != streamer.buffer_size - 1: return

    sorted_indicies = np.argsort(streamer.arrivals)
    streamer.sizes = streamer.sizes[sorted_indicies]
    streamer.arrivals = streamer.arrivals[sorted_indicies]

    streamer.output[2] += streamer.buffer_size

    for i in range(0, streamer.buffer_size-1):
        time1 = streamer.arrivals[i]
        time2 = streamer.arrivals[i+1]
        size2 = streamer.sizes[i+1]
        
        gap = (time2 - time1) - ((8 * size2) / streamer.link_bps)

        # Queuing packet
        if gap < 0:
            streamer.output[0] += (time1 + time2) / 2
        elif gap > 0.0005:
            streamer.output[1] += (time1 + time2) / 2       



def main():
    streamer = Streamer(params.data_file, params.window_size, output=[0, 0, 0], link_bps=params.link_bps)
    streamer.stream(queuing_info, skip=params.skip)
    print("Number Queued Packets: ", streamer.output[0])
    print("Number Large Gaps: ", streamer.output[1])
    print("Number of packets:", streamer.output[2])
 

if __name__ == "__main__":
    desc = "Calculates number of queued packet and number of large gaps"
    args = SetUpParser(desc)
    main()

