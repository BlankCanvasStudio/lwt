#!/bin/python3


import struct, os, random, sys
import numpy as np


# Read the files at the right point (a few trials at supect points
# Stolen from windowing ml code
def read_trial(trial_to_check, trial_num, start_time = 25, duration = 1):
    fname = '../ml/tiktok/cw-ow-timing-class/data/' + str(trial_to_check) + '-' + str(trial_num) + '/pipe_rcv.csv'
    fd = open(fname, 'rb')
    # size, time
    sequence = []

    fd.seek(4)
    offset = struct.unpack('d', fd.read(8))[0]
    file_size = os.path.getsize(fname)

    length = (file_size // 12) # 4 for int and 8 for double
    [ times, sizes] = [ np.zeros(length, dtype=np.float64), np.zeros(length, dtype=int) ]

    index = 0
    while fd.tell() < file_size:
        size = int.from_bytes(fd.read(4), sys.byteorder)
        time = struct.unpack('d', fd.read(8))[0]

        zerod_time = time - offset
        if zerod_time >= 0 and zerod_time >= start_time and zerod_time < start_time + duration:
            times[index] = time - offset
            sizes[index] = size

            index += 1

    fd.close()

    # Remove all values outside the int range
    mask = (times < -sys.maxsize - 1) | (times > sys.maxsize)
    # Convert values outside the range to zero
    times[mask] = 0


    return np.array(list(zip(times[:index + 1], sizes[:index + 1])))


def return_data(trials_to_check, num_trials, start_time = 25, duration = 1):
    for trial in trials_to_check:
        chosen = [ random.randint(0, 199) for _ in range(0,num_trials) ]
        for num in chosen:
            yield read_trial(trial, num, start_time, duration), trial, num
        

def get_gaps(data, link_bps = 100000000, thresh = 0.00000002, window = 10):

    output = [ [], [] ]

    gaps = np.zeros(window, dtype = 'd')

    for i in range(0, len(data) - 1):
        time1 = data[i][0]
        size1 = data[i][1]
        time2 = data[i + 1][0]
      
        new_gap = (time2 - time1) - ((8 * size1) / link_bps)

        gaps[ i % window ] = new_gap

        old_gap_loc = (i - 1) % window

        # See if there are any gaps
        sum = np.sum(gaps)
        if sum < thresh:
            gaps = np.ones(window, dtype=bool)

        shifting_value = gaps[old_gap_loc]

        if shifting_value == False:
            output[0] += [ time1 ] 
            output[1] += np.sum(gaps)

        gaps[(i + 1) % window] = False

    return output


def mean(values, precision):
    if len(values) == 0:
        return 0
    mean_value = np.mean(values)
    mean_value = np.format_float_positional(mean_value, precision=precision, unique=False, fractional=False, trim='k')
    return mean_value


def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0
  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg
  return out


def main():

    num_trials = 50
    trials_to_check = [ 0, 2, 3, 4 ]
    start_time = 25
    duration = 1
    precision = 8
    
    points_to_show = 20

    index = 0

    occurances = {}

    for data, trial, inst in return_data(trials_to_check, num_trials, start_time, duration):
        
        int_array = np.round(data).astype(int)

        unique_ints, per_sec = np.unique(int_array, return_counts=True)

        min_per_sec = min(per_sec)
        max_per_sec = max(per_sec)

        med_per_sec = np.percentile(per_sec, 50)
        
        max_value = np.max(data)




        first30out = data[range(0, 30)]
        # std_value = np.std(data)

        avg_in = np.sum(data)/float(len(data)) if len(data) else 0 


        avg_number_per_sec = np.sum(per_sec)/float(len(per_sec))

        chunks = data.reshape(1, -20)
        concentrations = np.empty(len(chunks))
        for i in range(len(chunks)):
            c = np.count_nonzero(chunks[i][1] == 1)
            concentrations[i] = c

        conc = concentrations

        alt_per_sec = [sum(x) for x in chunkIt(per_sec, 20)]
        altconc = [sum(x) for x in chunkIt(conc, 70)]

        print(min_per_sec, max_per_sec, med_per_sec, max_value, len(data), len(first30out), avg_number_per_sec, trial, inst)
        print(alt_per_sec)
        print(altconc)
        print(per_sec)
        print(len(data) * 2)
        print(sum(altconc))

#         # Plot the gaps to see anything
#         gaps = get_gaps(data)
#         # print('trial:', trial, ' inst: ', inst)
#         # print('gaps:', gaps)
# 
#         # Print the samples to see anything
#         # print(data[:points_to_show])
#     
#         means = mean(data, precision)
#         # print('mean:', means)
# 
# 
# 
#         if trial not in occurances:
#             occurances[trial] = {}
#         if means not in occurances[trial]:
#             occurances[trial][means] = 1
#         else:
#             occurances[trial][means] += 1
# 
# 
#         # if index == num_trials - 1:
#         #     print('\n')
# 
#         # index = (index + 1) % num_trials
#     for key, value in occurances.items():
#         print(key, ':')
#         for key2, value2 in value.items():
#             print('\n', key2, ': ', value2)
        


if __name__ == '__main__':
    main()


