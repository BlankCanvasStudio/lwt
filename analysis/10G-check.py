#!/bin/python3

import matplotlib.pyplot as plt

from config import *
import utils



def check_times(streamer):
    if streamer.insert_index == 0: return # going to use -1 indexing so won't work at 0

    time_between = streamer.arrivals[streamer.insert_index] - \
            streamer.arrivals[streamer.insert_index - 1]

    packet_size = streamer.sizes[streamer.insert_index]
    packet_size_bits = packet_size * 8

    print(packet_size_bits / (time_between))



def check_times_main(data_file):
    streamer = Streamer(params.data_file, params.window_size, link_bps=params.link_bps, output=[0, 0])
    streamer.stream(check_times, skip=params.skip)
    


def add_custom_parsing(parser):
    parser.add_argument("-x", "--example", 
        action="store_true",
        help="Does nothing. Arg is here in case I need custom parsing")


if __name__ == "__main__":
    desc = "Checks if the gaps recorded are possible on a 10G link, attempting to \
            simulate a 100M link."

    args = SetUpParser(desc, add_custom_parsing)

    check_times_main(args.data_file)

