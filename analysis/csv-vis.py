#!/bin/python3

import matplotlib.pyplot as plt

from config import *
import utils

def get_gap_times(streamer):
    if streamer.insert_index != streamer.buffer_size - 1: return

    sorted_indicies = np.argsort(streamer.arrivals)
    streamer.sizes = streamer.sizes[sorted_indicies]
    streamer.arrivals = streamer.arrivals[sorted_indicies]

    for i in range(0, streamer.buffer_size-1):
        ping = False
        time1 = streamer.arrivals[i]
        time2 = streamer.arrivals[i+1]
        size2 = streamer.sizes[i+1]
      
        gap = (time2 - time1) - ((8 * size2) / streamer.link_bps)

        streamer.output[0] += [ gap ]
        streamer.output[1] += [ (time1 + time2) / 2 ]
   

def main(ping_size = 0):
    if data_file.split('.')[-1] == 'pcap':
        streamer = utils.PcapStreamer(params.data_file, buffer_size = params.window_size, link_bps = params.link_bps, output = [[],[]])
    else:
        streamer = utils.Streamer(params.data_file, buffer_size = params.window_size, link_bps = params.link_bps, output = [[],[]])
    streamer.stream(get_gap_times, skip=params.skip)

    if ping_size:
        ping_time = (8 * ping_size) / streamer.link_bps
        plt.axhline(ping_time, color='green', linestyle='--', label='ping packet size')
    plt.scatter(x=streamer.output[1], y=streamer.output[0], color='red') #, s=0.5)
    plt.show()


def add_custom_parsing(parser):
    parser.add_argument("-p", "--pingsize", 
        default=0,
        help="Size of ping packets being sent over link. Used to draw \
                horiztonal line for identification purposes")

if __name__ == "__main__":
    desc = "Calculate the gaps in arrival data and plot them as the occured. \
            Y-axis the duration of the gap in sec and X is time of occurance"
    args = SetUpParser(desc, add_custom_parsing)

    main(int(args.pingsize))

