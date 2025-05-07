import os
import numpy as np
import re
import json
import struct
import sys
import traceback


def load_data(directory, delimiter='\t', file_split="-", length=10000, typ=2, unmon=False, processing='none'):
    """
    Load data from ascii files
    """
    X, y = [], []
    class_counter = 0
    for dir in os.listdir(directory):
        if not unmon:
            # Only use file names with a single dash in them?
            # files = [fname for fname in files if len(fname.split(file_split)) == 2]
            pass
        
        try:
            if unmon:
                trace_class = -1
            else:
                cls, inst  = dir.split(file_split)
                trace_class = int(cls)

            # build direction sequence
            [ size, times, direction ] = load_trace(os.path.join(directory, dir), length=length)

            if processing != 'none':
                [ size, times, direction ] = process_data(sizes, times, direction, processing)


            # This actually builds out the array
            # use time direction
            if typ==1:
                sequence = np.multiply(times, direction)
            # use time only
            elif typ==2:
                sequence = times.copy()
            # use direction only
            else:
                sequence = direction.copy()

            del size
            del times
            del direction

            sequence.resize((length, 1))
            X.append(sequence)
            y.append(trace_class)

        except Exception as e:
            print("Error for", dir)
            print(e)
            traceback.print_exc()
            print('\n\n')
            pass

    # wrap as numpy array
    X, Y = np.array(X), np.array(y)

    # print(X)
    # print(Y)

    # shuffle
    s = np.arange(Y.shape[0])
    np.random.seed(0)
    np.random.shuffle(s)
    X, Y = X[s], Y[s]

    # print(X)
    # print(Y)

    return X, Y


# Read the binary format and return an array of the timing array and sizing array
def read_data(path, length=5000):
    fd = open(path, 'rb')
    # size, time
    [ sizes, times, direction ] = [ np.zeros(length, dtype=int), np.zeros(length, dtype=np.float64), np.zeros(length, dtype=int) ]

    fd.seek(4)
    offset = struct.unpack('d', fd.read(8))[0]
    file_size = os.path.getsize(path)

    index = 0

    while fd.tell() < file_size and index < length:
        size = int.from_bytes(fd.read(4), sys.byteorder)
        time = struct.unpack('d', fd.read(8))[0]
        sizes[index] = size
        times[index] = time - offset
        index += 1

    fd.close()

    # Remove all values outside the int range
    mask = (times < -sys.maxsize - 1) | (times > sys.maxsize)
    # Convert values outside the range to zero
    times[mask] = 0

    return [ sizes, times, direction ]


def format_data(sizes, times):
    return times


# This reads a file and returns an array of arrays:
    # [ [timestamp],  [direction] ]
    # timstamp is a float
    # direction is either +1 or -1
def load_trace(path, seperator="\t", length=5000):
    """
    loads data to be used for predictions
    """

    [ sizes, times, direction ] = read_data(os.path.join(path, "pipe_rcv.csv"), length=length)

    # Cleans up data and does inference
    times = format_data(sizes, times)

    # Return the sequence data but no directionality can be found
    return [ sizes, times, direction ]


def gap_average(sizes, times):

    sizes_out = np.array([])
    times_out = np.array([])

    thresh = 0.00005
    len_gaps = 12
    link_bps = 100000000

    gaps = np.zeros(len_gaps)
    valid = np.zeros(params.window_size, dtype=bool)

    for i in range(1, len(times)):

        insert_index = i % len_gaps

        time1 = times[i - 1]
        time2 = times[i]
        size2 = sizes[i]

        old_gap = gaps[insert_index]

        new_gap = (time2 - time1) - ((8 * size2) / link_bps)
        gaps[insert_index] = new_gap

        # See if there are any gaps
        sum = np.sum(gaps)

        if sum < thresh:
            valid = np.ones(params.window_size, dtype=bool)

        shifting_value = valid[0]
        valid[:-1] = valid[1:]
        valid[-1] = False

        if shifting_value == False:
            approx_size = np.sum(gaps) * link_bps
            times_out = np.append(times_out, times[0])
            sizes_out = np.append(sizes_out, approx_size)

    return sizes_out, times_out



def process_data(sizes, times, direction, processing):

    if processing == 'none':
        return sizes, times, direction

    if processing == 'approx-arrival':
        sizes, times = gap_average(sizes, times)
        return sizes, times, direction

    return sizes, times, direction



