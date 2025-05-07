#!/bin/python3

import utils
from config import *

def pass_fn(streamer):
    total = 0
    if streamer.insert_index != streamer.buffer_size - 1: return
    for i in range(0, streamer.buffer_size-1):
        time1 = streamer.arrivals[i]
        time2 = streamer.arrivals[i+1]
        size2 = streamer.sizes[i+1]
        
        # print(size2)
        gap = (time2 - time1) - ((8 * size2) / streamer.link_bps)

        # print('time 1:', time1)
        # print('time 2:', time2)
        duration = time2 - time1
        if duration > 0.0001232 or duration < 0.0001168:
            # print('raw gap:\n', '\t@ ', time1, '\n', '\tduration: ', time2 - time1)
            total += 1
        # print('packet time:', ((8 * size2) / streamer.link_bps))
        # print('actual gap: ', gap)
        # print()
        # print(size2)
    
    streamer.sum += streamer.arrivals[-1] - streamer.arrivals[0]
    streamer.total += 1
    streamer.malform += total

def main():
    if data_file.split('.')[-1] == 'pcap':
        streamer = utils.PcapStreamer(params.data_file, buffer_size = params.window_size, link_bps = params.link_bps, output = [[], []])
    else:
        streamer = utils.Streamer(params.data_file, buffer_size = params.window_size, link_bps = params.link_bps, output = [[], []])

    streamer.sum = 0
    streamer.total = 0
    streamer.malform = 0

    streamer.stream(pass_fn, skip=params.skip)

    print("average window size: ", streamer.sum / streamer.total)
    print("Number of malformed windows: ", streamer.malform) 

def add_custom_parsing(parser):
    parser.add_argument("-z", "--zero", 
        action="store_true",
        help="placeholder argument")


if __name__ == "__main__":
    desc = "No Program implemented yet"

    args = SetUpParser(desc, add_custom_parsing)

    main()

