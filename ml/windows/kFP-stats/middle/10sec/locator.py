#!/bin/python3

import numpy as np
import os, struct, sys
import itertools # import pairwise

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


# Parse the file in memory very fast with limited ram
class Streamer:

    def __init__(self, filename, buffer_size = 100000, link_bps = 100 * 1000 * 1000, output = None, window_size = 10):
        self.filename = filename

        self.arrivals = np.zeros(buffer_size, dtype=np.double)
        self.sizes = np.zeros(buffer_size, dtype=int)
        self.buffer_size = buffer_size

        self.window_size = window_size

        self.insert_index = 0

        self.file_size = os.path.getsize(filename)

        self.link_bps = link_bps
        
        self.exit = False

        self.output = output

        with open(self.filename, 'rb') as fd:
            fd.seek(4)
            self.offset = struct.unpack('d', fd.read(8))[0]

        self.fd = open(self.filename, 'rb') 


    def stream(self, callback, skip = 0, align = True):
        self.fd.seek(0)
        self.fd.seek(skip * 12) # 4 byte int with 8 byte double

        while self.fd.tell() < self.file_size:
            # This reading method is correct
            int_val, float_val = self.read()

            if float_val < 10:
                continue

            if align:
                self.arrivals[self.insert_index] = float_val - self.offset
            else:
                 self.arrivals[self.insert_index] = float_val   
            self.sizes[self.insert_index] = int_val

            callback(self)           
            if self.exit: return

            self.insert_index = ((self.insert_index + 1) 
                                    % self.buffer_size)


    def read(self):
        int_val = int.from_bytes(self.fd.read(4), sys.byteorder)
        float_val = struct.unpack('d', self.fd.read(8))[0]
        return int_val, float_val


    # Used for relative indexing datapoints
    def index(self, index):
        new_index = (self.insert_index + index) % self.buffer_size
        if new_index < 0: new_index = self.buffer_size + new_index
        return self.sizes[new_index], self.arrivals[new_index]
 

def gap_average(streamer):

    # Skip until 9.7 seconds in cause we don't need to look for gaps any earlier

    if streamer.arrivals[streamer.insert_index] < 9.700000000:
        return

    # This is high so we know we can get data (unless its empty
    if streamer.arrivals[streamer.insert_index] > 22:
        streamer.exit = True
        return

    time1 = streamer.arrivals[streamer.insert_index - 1]
    time2 = streamer.arrivals[streamer.insert_index]
    size2 = streamer.sizes[streamer.insert_index]
  
    old_gap = streamer.gaps[streamer.insert_index]

    new_gap = (time2 - time1) - ((8 * size2) / streamer.link_bps)
    streamer.gaps[streamer.insert_index] = new_gap

    # See if there are any gaps
    val = np.sum(streamer.gaps)
    if val < streamer.thresh:
        streamer.tmp = np.ones(streamer.buffer_size, dtype=bool)

    shifting_value = streamer.tmp[0]
    streamer.tmp[:-1] = streamer.tmp[1:]
    streamer.tmp[-1] = False
    if shifting_value == False:
        streamer.output[0] += [ streamer.arrivals[streamer.insert_index] ]
        # streamer.output[1] += [ old_gap ]
        streamer.output[1] += [ np.sum(streamer.gaps) ]


def find_starting_gaps(data_file, window_size = 10, bps = 100000000, thresh = 0.00000002):

    streamer = Streamer(data_file, buffer_size = window_size, link_bps = bps, output = [[],[]])
    streamer.tmp = np.ones(window_size, dtype=bool)
    streamer.thresh = thresh
    streamer.gaps = np.zeros(window_size)
    streamer.stream(gap_average)

    return streamer.output[0]

def find_start_of_data(data_file, window_size = 10, bps = 100000000, thresh = 0.00000002):

    early_gap_location = sorted(list(set(find_starting_gaps(data_file, window_size, bps, thresh))))

    # This is calculating gaps between the packet detection gaps
    inter_packet_gaps = [ abs(x - y) for (x, y) in pairwise(early_gap_location) ] 

    start_time = early_gap_location[0] if len(early_gap_location) else -1
    if start_time == -1: return -1

    max_time = start_time + 4 + 0.1

    # Could add counting to this but it works just as well
    non_ping_index = -1
    for i, el in enumerate(inter_packet_gaps):

        if early_gap_location[i] <= max_time: # too quick after ping. This should be hit
            continue

        non_ping_index = i
        break

    if non_ping_index > 0:
        return early_gap_location[non_ping_index]

    return -1



if __name__ == "__main__":
    start_time = find_start_of_data("/home/test/Downloads/pipe_rcv.csv")
    print('start time: ', start_time)

