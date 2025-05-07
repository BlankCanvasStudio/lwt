#!/bin/python3

from utils import * 
import argparse

prefix = "../data-lwt/"
prefix += "baseline-1"
# prefix += "gmail-basic-recieving-4"
# prefix += "usec-test-0"
prefix += "/"

# data_file = prefix + "click-gen.pcap"
# data_file = prefix + "filled-router.pcap"
# data_file = prefix + "filled-router-out.pcap"
# data_file = prefix + "router-one.csv"
# data_file = prefix + "router-two.csv"
# data_file = prefix + "pipe_rcv.csv"
data_file = "/home/test/Downloads/pipe_rcv.csv"

window_size = 200000
link_bps = 100*(1000**2)
skip = 0


class DataStructure:
    def __init__(self, data_file, window_size, link_bps, skip):
        self.data_file   = data_file
        self.window_size = window_size
        self.link_bps    = link_bps
        self.skip        = skip
        self.file_is_csv = data_file[-3:] == 'csv'

params = DataStructure(
    data_file = data_file,
    window_size = window_size,
    link_bps = link_bps,
    skip = skip,
)

def SetUpParser(desc = "No Description Given", custom_arg_processing = None):

    global params 

    # Set up basic argument parser
    parser = argparse.ArgumentParser(description=desc)

    # Add default parsing
    parser.add_argument("data_file", nargs='?', default=params.data_file)
    # Parsing for window size
    parser.add_argument("-w", "--window", 
        type=int,
        help="Specify the window size to use in program",
        default=params.window_size)
    parser.add_argument("-s", "--skip", 
        type=int,
        help="Specify how many data points in program to skip before running",
        default=params.skip)
    parser.add_argument("-b", "--bps", 
        type=int,
        help="Specify the bps of the link",
        default=params.link_bps)

    # Add custom parsing
    if custom_arg_processing is not None:
        custom_arg_processing(parser)
        
    # Actually parse the arguments
    args = parser.parse_args()
    # Do default updates based on arguments
    params.data_file = str(args.data_file)
    params.window_size = int(args.window)
    params.skip = int(args.skip)
    params.link_bps = int(args.bps)
    params.file_is_csv = params.data_file[-3:] == 'csv'
    # Return args object
    return args

"""
if not file_is_csv:
    # Assuming file is a pcap
    pcap_reader = MinPCAPReader(data_file)
    times = pcap_reader.times(align = True)
    sizes = pcap_reader.sizes()
"""

