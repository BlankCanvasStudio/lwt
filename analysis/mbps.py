#!/bin/python3

import utils
from config import *

import matplotlib.pyplot as plt
import numpy as np
import struct
import binascii
import sys, os

from slice import gap_average


def calc_pipe_bps(streamer_in):
    if streamer_in.insert_index != streamer_in.buffer_size - 1: return
    streamer_in.output[0] += [ (8 * np.sum(streamer_in.sizes)) / (np.max(streamer_in.arrivals) - np.min(streamer_in.arrivals)) ]
    streamer_in.output[1] += [ streamer_in.arrivals[-1] - streamer_in.arrivals[0] ]


def pipe_main(print_info, bufferlen, linkrate):
    if data_file.split('.')[-1] == 'pcap':
        streamer = utils.PcapStreamer(params.data_file, buffer_size = bufferlen, link_bps = params.link_bps, output = [[], []])
    else:
        streamer = utils.Streamer(params.data_file, buffer_size = bufferlen, link_bps = params.link_bps, output = [[], []])

    streamer.bufferlen = bufferlen
    streamer.stream(calc_pipe_bps, skip=params.skip)
    
    if print_info:
        for el in streamer.output[0]:
            print(el)
    else:
        if linkrate:
            plt.axhline(linkrate, color='green', linestyle='--', label='expected bps')
        plt.scatter(x=streamer.output[1], y=streamer.output[0])
        plt.show()
 

def tap_main(print_info, bufferlen, linkrate):
    # Find the large gaps & their sizes
    streamer = Streamer(params.data_file, buffer_size = params.window_size, link_bps = params.link_bps, output = [[],[]])
    streamer.tmp = np.zeros(params.window_size, dtype=bool)
    streamer.thresh =  0.00000002
    streamer.stream(gap_average, skip=params.skip)
    
    arrivals = streamer.output[0]
    gaps = streamer.output[1]

    scratch_arrivals = np.zeros(bufferlen)
    scratch_gaps = np.zeros(bufferlen)

    output_bps = []
    output_times = []

    for i in range(0, len(arrivals)):
        index = i % bufferlen

        scratch_arrivals[index] = arrivals[i]
        scratch_gaps[index] = gaps[i]

        if index != 0: continue

        bits = np.sum(scratch_gaps) * params.link_bps
        duration = (np.max(scratch_arrivals) - np.min(scratch_arrivals))
        est_time = (np.max(scratch_arrivals) + np.min(scratch_arrivals)) / 2


        
        output_bps += [ bits / duration ]
        output_times += [ est_time ]

    if print_info:
        for i in range(0, len(output_bps)):
            print(output_times[i], output_bps[i])
    else:
        if linkrate:
            plt.axhline(linkrate, color='green', linestyle='--', label='expected bps')
        plt.scatter(x=output_times, y=output_bps)
        plt.show()



def add_custom_parsing(parser):
    parser.add_argument("-t", "--tapped", 
        action="store_true",
        help="Calculate the mbps of tapped client")
    parser.add_argument("-p", "--print", 
        action="store_true",
        help="Print the data instead of plotting it")
    parser.add_argument("-l", "--bufferlen", 
        default=5,
        help="Specify how many gaps should be used to calculate instantaneous bps")
    parser.add_argument("-r", "--linkrate", 
        default=0,
        help="Specify the expected bps, so a reference line can be plotted")


if __name__ == "__main__":
    desc = "Calculate the gaps in arrival data and plot them as the occured. \
            Y-axis the duration of the gap in sec and X is time of occurance"
    args = SetUpParser(desc, add_custom_parsing)

    if args.tapped:
        tap_main(args.print, int(args.bufferlen), int(args.linkrate))
    else:
        pipe_main(args.print, int(args.bufferlen), int(args.linkrate))

