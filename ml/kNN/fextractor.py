import sys
import subprocess
import numpy
import os
from loaders import *
import struct
import numpy as np
import threading
import traceback

def extract(times, sizes, features):

    # print('feature one')

    #Transmission size features
    features.append(len(sizes))

    # count = 0
    # for x in sizes:
    #     if x > 0:
    #         count += 1

    count = np.sum(sizes > 0)
    features.append(count)
    features.append(len(times)-count)

    features.append(times[-1] - times[0])

    #Unique packet lengths
##    for i in range(-1500, 1501):
##        if i in sizes:
##            features.append(1)
##        else:
##            features.append(0)

    #Transpositions (similar to good distance scheme)
    # count = 0
    # for i in range(0, len(sizes)):
    #     if sizes[i] > 0:
    #         count += 1
    #         features.append(i)
    #     if count == 500:
    #         break
    # for i in range(count, 500):
    #     features.append("X")
        

    # print('feature two')
    # There is no directional data so this gets ignored
    count = 500
    features.append(["X"] * count)
 
    # count = 0
    # prevloc = 0
    # for i in range(0, len(sizes)):
    #     if sizes[i] > 0:
    #         count += 1
    #         features.append(i - prevloc)
    #         prevloc = i
    #     if count == 500:
    #         break
    # for i in range(count, 500):
    #     features.append("X")
 
    # count = 0
    # prevloc = 0
    # for i in range(0, len(sizes)):
    #     if sizes[i] > 0:
    #         count += 1
    #         features.append(i - prevloc)
    #         prevloc = i
    #     if count == 500:
    #         break

    # print('feature three')
    count = 500
    features += [ i for i in range(0, count) ]
    for i in range(count, 500):
        features.append("X")


    # print('feature four')
    #Packet distributions (where are the outgoing packets concentrated)
    # count = 0
    # for i in range(0, min(len(sizes), 3000)):
    #     if i % 30 != 29:
    #         if sizes[i] > 0:
    #             count += 1
    #     else:
    #         features.append(count)
    #         count = 0
    # for i in range(int(len(sizes)/30), 100):
    #     features.append(0)

    features.append([30] * min(len(sizes), 3000))
    features.append([0] * (int(len(sizes)/30) // 100))

    # print('feature five')    
    #Bursts
    bursts = []
    curburst = 0
    consnegs = 0
    stopped = 0

    curburst += np.sum(sizes)
    # for x in range(0, len(sizes) // 3):
    #     if x < 0:
    #         consnegs += 1
    #         if (consnegs == 2):
    #             bursts.append(curburst)
    #             curburst = 0
    #             consnegs = 0
    #     if x > 0:
    #         consnegs = 0
    #         curburst += x

    # print('feature six')    
    if curburst > 0:
        bursts.append(curburst)

    if (len(bursts) > 0):
        features.append(max(bursts))
        features.append(numpy.mean(bursts))
        features.append(len(bursts))
    else:
        features.append("X")
        features.append("X")
        features.append("X")
##    print bursts

    # print('feature seven')
    counts = [0, 0, 0, 0, 0, 0]
    for x in bursts:
        if x > 2:
            counts[0] += 1
        if x > 5:
            counts[1] += 1
        if x > 10:
            counts[2] += 1
        if x > 15:
            counts[3] += 1
        if x > 20:
            counts[4] += 1
        if x > 50:
            counts[5] += 1
    features.append(counts[0])
    features.append(counts[1])
    features.append(counts[2])
    features.append(counts[3])
    features.append(counts[4])
    features.append(counts[5])

    # print('feature eight')
    for i in range(0, 100):
        try:
            features.append(bursts[i])
        except:
            features.append("X")

    # print('feature nine')
    for i in range(0, 10):
        try:
            features.append(sizes[i] + 1500)
        except:
            features.append("X")


    # print('feature ten')
    itimes = times[1:] - times[:-1]
    # itimes = [0]*(len(sizes)-1)
    # for i in range(1, len(sizes)):
    #     itimes[i-1] = times[i] - times[i-1]

    # print('feature eleven')
    if len(itimes) > 0:
        features.append(numpy.mean(itimes))
        features.append(numpy.std(itimes))
    else:
        features.append("X")
        features.append("X")

def flog(msg, fname):
    f = open(fname, "a+")
    f.write(repr(time.time()) + "\t" + str(msg) + "\n")
    f.close()


def read_data(path):
    fd = open(path, 'rb')

    fd.seek(4)
    offset = struct.unpack('d', fd.read(8))[0]
    file_size = os.path.getsize(path)
    data_points = file_size // 12 # 4 for int and 8 for double

    [ sizes, times ] = [ np.zeros(data_points, dtype=int), np.zeros(data_points, dtype=np.float64) ]

    index = 0

    while fd.tell() < file_size:
        size = int.from_bytes(fd.read(4), sys.byteorder)
        time = struct.unpack('d', fd.read(8))[0]
        sizes[index] += size
        times[index] += time - offset
        index += 1

    fd.close()

    # Remove all values outside the int range
    mask = (times < -sys.maxsize - 1) | (times > sys.maxsize)
    # Convert values outside the range to zero
    times[mask] = 0

    return [ sizes, times ]


def write_features(fname):
    try:
        if "-0.cell" in fname:
            print(fname)
        tname = fname + "kNN"




        """
            THIS IS WHERE WE HAVE TO OVERWRITE LOADING THE DATA
        """


        #load up times, sizes
        # times = np.array([])
        # sizes = np.array([])
        # f = open(fname, "r")
        # for x in f:
        #     x = x.split("\t")
        #     times.append(float(x[0]))
        #     sizes.append(int(x[1]))
        # f.close()



        """ 
            This should work wonderfully
        """

        [ sizes, times ] = read_data(fname)


        #Extract features. All features are non-negative numbers or X. 
        features = []
        extract(times, sizes, features)
        writestr = ""

        for x in features:
            if x == 'X':
                x = -1
            writestr += (repr(x) + "\n")
        fout = open(tname, "w")
        fout.write(writestr[:-1])
        fout.close()

        print("loaded file", fname)
    except Exception as e:
        traceback.print_exc()
        print(e)


def main(optfname):

    # sys.argv = ["", "options-temp"]
    try:
        optfname = sys.argv[1]
        d = load_options(optfname)
    except Exception as e:
        print(sys.argv[0], str(e))
        sys.exit(0)

    [ trainlist, testlist ] = get_list(d)
    flat_trainlist = [ a for s in trainlist for a in s ]
    flat_testlist = [ a for s in testlist for a in s ]
    flist = flat_trainlist + flat_testlist


    THREAD_NUM = 50 


    threads = []


    print("fextractor.py: Extracting features")
    for fname in flist:
        # Create a thread for each function call
        # thread = threading.Thread(target=write_features, args=(fname,))
        # threads.append(thread)
        # thread.start()

        process = subprocess.Popen(["python3", "-c", f"from fextractor import write_features; write_features('{fname}')"])
        threads += [ process ]

        if len(threads) < THREAD_NUM:
            continue

        # Wait for all threads to finish
        # Wait for all threads to finish
        for thread in threads:
            thread.wait()

        # Terminate and wait for all threads
        for thread in threads:
            thread.terminate()
            thread.wait()
        threads = []

if __name__=="__main__":
    main()

