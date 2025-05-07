#!/bin/python3

import matplotlib.pyplot as plt

import utils
from config import *


def main():
    def pass_fn(streamer):
        pass

    if data_file.split('.')[-1] == 'pcap':
        streamer = utils.PcapStreamer(params.data_file, buffer_size = params.window_size, link_bps = params.link_bps, output = [[],[]])
    else:
        streamer = utils.Streamer(params.data_file, buffer_size = params.window_size, link_bps = params.link_bps, output = [[],[]])

    streamer.stream(pass_fn, skip = params.skip)

    del streamer.sizes

    plt.title(data_file.split('/', 2)[2])
    plt.scatter(x=streamer.arrivals, y=np.zeros(params.window_size), s=0.5)
    plt.show()


if __name__ == "__main__":
    args = SetUpParser("Plot arrival times of packets")
    main()

