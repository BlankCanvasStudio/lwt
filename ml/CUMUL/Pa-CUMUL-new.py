#!/bin/python3
import subprocess
import math
import sys
import time
from loaders import *
import numpy as np, traceback
# from gen_list import *


np.seterr(invalid='raise')
np.set_printoptions(threshold=np.inf)



def flog(msg, fname):
    f = open(fname, "a+")
    f.write(str(msg) + "\n")
    f.close()    


def log(*args):
    msg = ' '.join(map(str, args))
    print(msg)
    LOG_FILE = d["OUTPUT_LOC"] + '/' + 'c' + str(d["CLOSED_SITENUM"]) + '-i' + str(d["CLOSED_INSTNUM"]) + '-o' + str(d["OPEN_SITENUM"]) + '-i' + str(d["OPEN_INSTNUM"]) + '/' + 'log.txt'
    flog(msg, LOG_FILE)


"""
    Please implement this. Use sizes as y and times as x
        then do the prediction
"""
def size_extract(sinste, interpolants = 100):
    #sinste: list of packet sizes

    sinste = np.array(sinste)

    insize = len(sinste[sinste > 0])            # sum total of packets out
    outsize = len(sinste[sinste < 0])                     # sum total of packets out
    inpacket = np.sum(sinste[0, sinste[0,:] > 0])  # sum total of all packet sizes in
    outpacket = np.sum(sinste[0, sinste[0,:] < 0])                   # sum total of all packet sizes out

    features = np.array([insize, outsize, inpacket, outpacket])


    n = num_points #number of linear interpolants. Estimating derivatives newton style

    x = np.cumsum(np.abs(sinste[:,0]))
    y = np.cumsum(sinste[:,0])
    graph = np.column_stack((x,y))


    # # derive interpolants
    gap = float(np.max(graph[:, 0])) / n


    # # Make estimated graph, assuming linear
    tmp_x = np.full(n, gap)
    est_x = np.cumsum(tmp_x) # This is correct. Plays role of next_x


    # Find all locations where x is greater than approx x. Don't allow out of bounds indexing
    x_greater_loc = np.array([ np.searchsorted(x, i, side='right') for i in est_x ])
    x_greater_loc[x_greater_loc >= len(x)] = len(x) - 1

    # Calculate the slope at every point in real data (only need points at interpolation)
    numerator   = graph[x_greater_loc, 1] - graph[x_greater_loc - 1, 1] # next_pt_y - cur_pt_y
    denominator = graph[x_greater_loc, 0] - graph[x_greater_loc - 1, 0]

    # Calculate the slope & cover the edge case
    slope = np.array(numerator / denominator)
    slope[np.where(np.isnan(slope))] = 1000

    # A series of approximations of what y should be
    next_y_array = (slope * (est_x - graph[x_greater_loc - 1, 0])) + graph[x_greater_loc - 1, 1]
 
    interpolants = ( next_y_array[1:] - next_y_array[:-1] ) / gap

    features = np.append(features, interpolants)

    return features


def extract(sinste, num_points = 100):
    #sinste: list of packet sizes

    inpacket  = len(sinste[sinste > 0])            # sum total of packets out
    outpacket = len(sinste[sinste < 0])                     # sum total of packets out
    insize = np.sum(sinste[0, sinste[0,:] > 0])  # sum total of all packet sizes in
    outsize = np.sum(sinste[0, sinste[0,:] < 0])                   # sum total of all packet sizes out

    features = np.array([insize, outsize, inpacket, outpacket])


    n = num_points #number of linear interpolants. Estimating derivatives newton style

    x = np.cumsum(np.abs(sinste[:,0]))
    y = np.cumsum(sinste[:,0])
    graph = np.column_stack((x,y))


    # # derive interpolants
    gap = float(np.max(graph[:, 0])) / n


    # # Make estimated graph, assuming linear
    tmp_x = np.full(n, gap)
    est_x = np.cumsum(tmp_x) # This is correct. Plays role of next_x


    # Find all locations where x is greater than approx x. Don't allow out of bounds indexing
    x_greater_loc = np.array([ np.searchsorted(x, i, side='right') for i in est_x ])
    x_greater_loc[x_greater_loc >= len(x)] = len(x) - 1

    # Calculate the slope at every point in real data (only need points at interpolation)
    numerator   = graph[x_greater_loc, 1] - graph[x_greater_loc - 1, 1] # next_pt_y - cur_pt_y
    denominator = graph[x_greater_loc, 0] - graph[x_greater_loc - 1, 0]

    # Calculate the slope & cover the edge case
    slope = np.array(numerator / denominator)
    slope[np.where(np.isnan(slope))] = 1000

    # A series of approximations of what y should be
    next_y_array = (slope * (est_x - graph[x_greater_loc - 1, 0])) + graph[x_greater_loc - 1, 1]
 
    interpolants = ( next_y_array[1:] - next_y_array[:-1] ) / gap

    features = np.append(features, interpolants)

    return features


try:
    optfname = sys.argv[1] if sys.argv[1] else 'options.txt'
    # Returns a dictionary of options
    d = load_options(optfname)
except Exception as e:
    print("Error loading arguments. Did you pass in options file?")
    print(sys.argv[0], str(e))
    sys.exit(0)
 

of = d["OUTPUT_LOC"] + '/c' + str(d["CLOSED_SITENUM"]) + '-i' + str(d["CLOSED_INSTNUM"]) + '-o' + str(d["OPEN_SITENUM"]) + '-i' + str(d["OPEN_INSTNUM"])

if not os.path.exists(d["OUTPUT_LOC"]):
    os.mkdir(d["OUTPUT_LOC"])

if not os.path.exists(of):
    os.mkdir(of)


# Do some logging
log(sys.argv[0] + " " + sys.argv[1])
log(repr(d))


[tpc, tnc, nc, pc] = [0, 0, 0, 0]

ofname = of + '/data' # + sys.argv[0]
confname = of + '/' + "svm-conf.results"

if os.path.exists(confname):
    log('remove old data file before running')
    sys.exit()


skipext = 0
if "DO_NOT_EXTRACT" in d:
    if d["DO_NOT_EXTRACT"] == 1:
        skipext = 1

trainext = ofname + ".train"
testext = ofname + ".test"



"""

    THIS IS WHAT WE NEED TO IMPROVE. THIS IS HOW WE BUILD TESTING DATASET

"""


# This function seems to be building the dataset?
# Only writes the features return from extract() after reading in the data file
# Read the comments to figure out the file type
if (skipext == 0):

    # Build lists of files and separate them into folders
    if (d["GEN_OWN_LIST"] == 1):
        # gen_list(d)
        get_list(d)

    trainnames, testnames = get_list(d)

    # testnames and trainnames are array where each index is an array of different trials
    # The trials all have a testname (string ?)
    # traindata, trainnames = get_list(d["TRAIN_LIST"])
    # testdata, testnames = get_list(d["TEST_LIST"])
    log("Extracting features...")
    #extract features
    fullnames = [trainnames, testnames]
    fullexts = [trainext, testext] # These are auto created. WON'T OVERWRITE DATA
    # Iterate over testing and training
    for type_i in range(0, 2):
        # Open a datafile to store the data
        fout = open(fullexts[type_i], "w")
        # Iterate over all the sites
        for ci in range(0, len(fullnames[type_i])): # Iterate over training & testing
            log("Site {} of {}".format(ci, len(fullnames[type_i])))
            for ti in range(0, len(fullnames[type_i][ci])): # Iterate over instance recordings

                """
                    This section builds data files using specification is libsvm
                """
                try:
                    # Extract the data `fullnames[type_i][ci][ti]` is a filename
                    cells = load_cell(fullnames[type_i][ci][ti], ext='.csv') # returns [ [ time, size ] ]
                    # Apparently this needs to be a list of packet sizes
                    feats = extract(cells, num_points = 100)
                    # feats = [ num packets in, num packets out, total packet size in, total packet size out ]
                    fout.write(str(ci)) # This is the number of site is is
                    for fi in range(0, len(feats)):
                        fout.write(" " + str(fi+1) + ":" + str(feats[fi])) # Now actually write the data
                    fout.write("\n")
                except:
                    log('failed to load trial: ', fullnames[type_i][ci][ti])
                    pass
        fout.close()



# Set SVM_C_LOG and G_LOG
"""
    YOU NEED TO SET THESE WELL APPARENTLY
"""
if not("SVM_C_LOG" in d and "SVM_G_LOG" in d):
    d["SVM_C_LOG"] = 10
    d["SVM_G_LOG"] = -15
SVM_C = math.pow(2.0, d["SVM_C_LOG"])
SVM_G = math.pow(2.0, d["SVM_G_LOG"])



# So they completely outsource building the SVM. Thats cool I suppose
log("Start training...")
cmd = "../libsvm/svm-train -c {1} -g {2} {3} {0}.model".format(
    ofname, SVM_C, SVM_G, trainext)
subprocess.call(cmd, shell=True)
log("Start testing...")

# Usage: svm-predict [options] test_file model_file output_file

# cmd = "../libsvm/svm-predict -o {1} {2} {0}.model {0}.svmlog".format(
#     ofname, confname, testext)
# subprocess.call(cmd, shell=True)

cmd = "../libsvm/svm-predict {2} {0}.model {1}".format(
    ofname, confname, testext)
subprocess.call(cmd, shell=True)


# This section is reading the predictions and getting things like TPR and FPR from them
guesses = np.array([ int(x.strip()) for x in open(confname, "r").readlines() ])
answers = np.array([ int(x.strip().split(' ')[0]) for x in open(testext, "r").readlines() ])

num_classes = len(np.unique(answers))

correct_guesses = np.array(guesses == answers)
incorrect_guesses = np.array(correct_guesses == False)

def TP(c):
    return np.count_nonzero(correct_guesses[answers == c])

def FP(c):
    return np.count_nonzero(incorrect_guesses[guesses == c])

def FN(c):
    return  np.count_nonzero(incorrect_guesses[answers == c])

def TN(c):
    return np.count_nonzero(correct_guesses[answer != c])

# Accuracy, precision, recall, f1, and aoc_roc

# Acc = # correct / Total #
def AccuracyForClass(c):
    denom = np.count_nonzero(guesses == c)
    if not denom: return -1
    return TP(c) / denom

# Precision = TP / (TP + FP). This is per class
def PrecisionForClass(c):
    denom = (TP(c) + FP(c))
    if not denom: return -1
    return TP(c) / denom
# Recall = TP / (TP + FN). This is per class
def RecallForClass(c):
    denom = (TP(c) + FN(c))
    if not denom: return -1
    return TP(c) / denom


# F1 = 2 (Precision * Recall) / (Precision + Recall). This is per class
def F1ForClass(c):
    denom =  (PrecisionForClass(c) + RecallForClass(c))
    if not denom: return -1
    return 2 * (PrecisionForClass(c) * RecallForClass(c)) / denom

# Just helpful for me to visualize
def GenerateConfMatrix():
    conf_matrix = np.zeros((num_classes, num_classes))

    for i, el in enumerate(guesses):
        conf_matrix[answers[i], el] += 1

    return conf_matrix

# Print the stats
log('\n')

for i in range(0, num_classes):
    log(f'Accuracy for class {i}:', AccuracyForClass(i))

log('\n')

for i in range(0, num_classes):
    log(f'Precision for class {i}:', PrecisionForClass(i))

log('\n')

for i in range(0, num_classes):
    log(f'Recall for class {i}:', RecallForClass(i))

log('\n')

for i in range(0, num_classes):
    log(f'F1for class {i}:', F1ForClass(i))

log('\n')


#np.set_logoptions(threshold=np.inf)

log(GenerateConfMatrix())
log('vertical is what was actually guessed')

