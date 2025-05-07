#!/bin/python3

import matplotlib.pyplot as plt

from config import *
import utils

gaps = {}
gaps_to_sec = {}


def count_gaps(streamer):
    if streamer.insert_index != 0: return

    global gaps
    global gaps_to_sec

    sorted_indicies = np.argsort(streamer.arrivals)
    streamer.sizes = streamer.sizes[sorted_indicies]
    streamer.arrivals = streamer.arrivals[sorted_indicies]

    for i in range(0, len(streamer.sizes)-1):
        time1 = streamer.arrivals[i]
        time2 = streamer.arrivals[i+1]
        
        if time1 < 5: continue

        gap = time2 - time1

        if gap not in gaps:
            gaps[gap] = 0
            gaps_to_sec[gap] = []
            
        gaps[gap] += 1
        gaps_to_sec[gap] += [ time1 + (gap / 2) ]
 

def calc_dead_time(streamer):
    if streamer.insert_index != streamer.buffer_size - 1: return

    sorted_indicies = np.argsort(streamer.arrivals)
    streamer.sizes = streamer.sizes[sorted_indicies]
    streamer.arrivals = streamer.arrivals[sorted_indicies]

    for i in range(0, streamer.buffer_size-1):
        time1 = streamer.arrivals[i]
        time2 = streamer.arrivals[i+1]
        size2 = streamer.sizes[i+1]
        
        gap = (time2 - time1) - ((8 * size2) / streamer.link_bps)

        if gap > 0:
            streamer.output[0] += gap
        else:
            streamer.output[1] -= gap



def dead_time_main():
    streamer = Streamer(params.data_file, params.window_size, output=[0, 0], link_bps=params.link_bps)
    streamer.stream(calc_dead_time, skip=params.skip)
    print("Positive dead time: ", streamer.output[0])
    print("Negative dead time: ", streamer.output[1])
 


def count_gaps_main():
    streamer = Streamer(params.data_file, params.window_size, link_bps=params.link_bps, output=[0, 0])
    streamer.stream(count_gaps, skip=params.skip)
    for item, index in sorted(gaps.items()):
        print(item, index)
    # Could also print gaps_to_sec array


def add_custom_parsing(parser):
    parser.add_argument("-d", "--deadtime", 
        action="store_true",
        help="Calculate the cumulative postive and negative dead time for file")
    parser.add_argument("-g", "--countgaps", 
        action="store_true",
        help="Calculate the number of occurances of each gap duration \
                        (can be used to build a historgram). Also \
                        calculates the times when those gaps occur")

if __name__ == "__main__":
    desc = "Can calculate the dead time gaps and generates a dictionaries: \
            dict[gap durations]=(number of occurances) as well as \
            dict[gap durantions]=(time of occurances) and prints them"

    args = SetUpParser(desc, add_custom_parsing)

    if args.tapped:
        tap_main(args.print, int(args.bufferlen), int(args.linkrate))
    else:
        pipe_main(args.print, int(args.bufferlen), int(args.linkrate))

    if args.deadtime:
        dead_time_main()
    if args.countgaps:
        count_gaps_main()

