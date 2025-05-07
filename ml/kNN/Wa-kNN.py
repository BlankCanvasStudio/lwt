#!/bin/python3

import subprocess
import sys
import time
from loaders import *
import traceback
        
# Loads all the cli arguments
# NOTE: The file name used here actually changes
try:
    optfname = sys.argv[1] if sys.argv[1] else 'options.txt'
    d = load_options(optfname)
    ofname = "{}{}-{}".format(d["OUTPUT_LOC"], "Wa-kNN", d["CORE_NAME"])
except Exception as e:
    print(sys.argv[0], str(e))
    traceback.print_exc()
    sys.exit(0)

try:
    # Create a log of the file options used here
    logfname = ofname + ".log"
    flog(sys.argv[0] + " " + sys.argv[1], logfname, logtime=1)
    flog(repr(d), logfname)


    ##if "CORE_NAME" in d:
    ##    froot = "{}{}-{}".format(d["OUTPUT_LOC"], sys.argv[0], d["CORE_NAME"])
    ##else:
    ##    froot = "{}{}".format(d["OUTPUT_LOC"], sys.argv[0])
    ##


    # Update the filenames
    d["TRAIN_LIST"] = ofname + "-trainlist"
    d["TEST_LIST"] = ofname + "-testlist"
    d["WEIGHT_LIST"] = ofname + "-weightlist"


    # trainnames is an array where trainnames[i] is a list of filenames of website i
    trainnames, testnames = get_list(d)


    #flatten trainnames, testnames
    trainnamesf = [f for x in trainnames for f in x]
    testnamesf = [f for x in testnames for f in x]


    # write filelist for flearner. These are all the 
    f = open(d["TRAIN_LIST"], "w")
    for name in trainnamesf:
        f.write(name + "\n")
    f.close()
    f = open(d["WEIGHT_LIST"], "w")
    for name in trainnamesf:
        f.write(name + "\n")
    f.close()
    f = open(d["TEST_LIST"], "w")
    for name in testnamesf:
        f.write(name + "\n")
    f.close()


    # Below fundamentally writes a config file for you

    print("Writing options")

    #write new options file used for flearner
    #we need to do this to write out the train/weight/test list
    write_options(ofname + "flearner-options", d)

    print("Calling feature extractor")

    

    print(optfname)
    # import fextractor

    # fextractor.main(optfname)
    d = load_options(optfname)

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
            thread.terminate()
            thread.wait()

        threads = []



    # cmd = "python fextractor.py " + optfname + "flearner-options"
    # cmd = "python3 fextractor.py " + optfname
    # subprocess.call(cmd, shell=True)

    print("calling flearner")

    cmd = "./flearner " + ofname + "flearner-options"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)

    for line in process.stdout:
        print(line, end='')

    for line in process.stderr:
        print(line, end='')

    process.wait()

    ##f = open("flearner.log", "r")
    ##lines = f.readlines()
    ##f.close()
    ##for line in lines:
    ##    log(line[:-1])

    ##f = open(flname, "r")
    ##lines = f.readlines()
    ##f.close()
    ##for line in lines:
    ##    rlog(line)

    ##for i in range(0, len(lines)):
    ##    line = lines[i]
    ##    if "Training time" in line:
    ##        time = float(line.split("\t")[1])
    ##        lines[i] = "Training time\t" + str(time + extracttime) + "\n"
    ##    if "Testing time" in line:
    ##        time = float(line.split("\t")[1])
    ##        lines[i] = "Testing time\t" + str(time + extracttime) + "\n"
except Exception as e:
    print(e)
    traceback.print_exc()

