#!/bin/python3

from utils import *
from config import *

# thresh = 0.000005
thresh = 0.00000002
gaps = np.zeros(params.window_size)

def gap_average(streamer):

    global gaps

    time1 = streamer.arrivals[streamer.insert_index - 1]
    time2 = streamer.arrivals[streamer.insert_index]
    size2 = streamer.sizes[streamer.insert_index]
  
    old_gap = gaps[streamer.insert_index]

    new_gap = (time2 - time1) - ((8 * size2) / streamer.link_bps)
    gaps[streamer.insert_index] = new_gap

    # See if there are any gaps
    sum = np.sum(gaps)
    if sum < streamer.thresh:
        streamer.tmp = np.ones(params.window_size, dtype=bool)

    shifting_value = streamer.tmp[0]
    streamer.tmp[:-1] = streamer.tmp[1:]
    streamer.tmp[-1] = False
    if shifting_value == False:
        streamer.output[0] += [ streamer.arrivals[0] ]
        # streamer.output[1] += [ old_gap ]
        streamer.output[1] += [ np.sum(gaps) ]


def main(print_in):
    streamer = Streamer(params.data_file, buffer_size = params.window_size, link_bps = params.link_bps, output = [[],[]])
    streamer.tmp = np.zeros(params.window_size, dtype=bool)
    streamer.thresh = thresh
    streamer.stream(gap_average, skip=params.skip)
    
    if print_in:
        for i, el in enumerate(streamer.output[0]):
            print(el, streamer.output[1][i])
    else:
        x_axis = streamer.output[0]
        y_axis = streamer.output[1]
        plt.scatter(x=x_axis, y=y_axis)
        plt.show()


 

def add_custom_parsing(parser):
    parser.add_argument("-p", "--print", 
        action="store_true",
        help="prints the data instead of plotting it")


if __name__ == "__main__":
    desc = "Identifies packet gaps in data. See code for details"

    args = SetUpParser(desc, add_custom_parsing)
    main(bool(args.print))

