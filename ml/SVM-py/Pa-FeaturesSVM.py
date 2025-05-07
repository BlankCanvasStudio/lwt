#!/bin/python3
import subprocess
import math
import sys
import time
from loaders import *
import numpy as np
import traceback
from sklearn import svm
# from gen_list import *


np.set_printoptions(threshold=np.inf)

d = {}

def flog(msg, fname):
    f = open(fname, "a+")
    f.write(str(msg) + "\n")
    f.close()    

def log(*args):
    global d
    msg = ' '.join([ str(x) for x in list(args) ])
    print(msg)
    LOG_FILE = d["OUTPUT_LOC"] + '/' + 'c' + str(d["CLOSED_SITENUM"]) + '-i' + str(d["CLOSED_INSTNUM"]) + '-o' + str(d["OPEN_SITENUM"]) + '-i' + str(d["OPEN_INSTNUM"]) + '/' + 'log.txt'
    flog(msg, LOG_FILE)



    
def extract(sinste, mbps = 100000000, window = 10, thresh = 0.00000002):

    sinste = np.array(sinste)

    #input "sinste" is a list of cells
    features = np.array([])
    

    #SIZE MARKERS
    #does not do anything for cells; see number markers
    features = np.append(features, np.zeros(300))


    # Build estimated packet arrivals from gaps
    num_subs = len(sinste) // window
    times_sub = np.split(sinste[:num_subs * window, 0], num_subs)
    sizes_sub = np.split(sinste[:num_subs * window, 1], num_subs)

    approx_times = np.array([ np.mean(subarray) for subarray in times_sub ])
    expected_times = np.array([ (np.sum(subarray) / mbps) for subarray in sizes_sub ])
    times_taken = np.array([ np.ptp(subarray) for subarray in times_sub ])

    deltas = np.abs(expected_times - times_taken)

    del expected_times
    del times_taken

    detection_mask = np.where(deltas > thresh)
    detection_times = approx_times[ detection_mask ]
    detection_sizes = deltas * mbps

    del approx_times
    del deltas
    del detection_times

    #HTML SIZE
    #this almost certainly doesn't actually give html document size
    features = np.append(features, np.sum(detection_sizes))

    del detection_sizes

    #TOTAL TRANSMITTED BYTES
    features = np.append(features, np.sum(sinste[sinste[:,1] < 0,1])) # Incoming
    features = np.append(features, np.sum(sinste[sinste[:,1] > 0,1])) # Outgoing


    #NUMBER MARKERS
    max_markers = 300
    # Append the detection mask cause its the location where packets appeared
    # Very cheeky. Could also do times
    markers = np.append(detection_mask, np.zeros(max_markers))[:max_markers]
    features = np.append(features, markers)

    del markers
    

    # NUM OF UNIQUE PACKET SIZES
    # Should build packet sizes earlier and use as html approximation
    features = np.append(features, len(np.unique(sizes_sub)))


    #PERCENTAGE INCOMING PACKETS
    features = np.append(features, 1)


    #NUMBER OF PACKETS
    features = np.append(features, len(sizes_sub))

    features = np.append(features, times_sub)

    return features


def read_feats(fname):
    feats = []
    with open(fname, "r") as f:
        lines = f.readlines()
        for line in lines:
            this_feat = []
            li = line.split(" ")[1:]
            for l in li:
                l = l.split(":")[1]
                this_feat.append(float(l))
            feats.append(this_feat)
    return feats

def dist(cell1, cell2):
    #does not implement high dimensionality kernel trick?
    feat1 = extract(cell1)
    feat2 = extract(cell2)

    dist = 0
    for i in range(0, min(len(feat1), len(feat2))):
        dist += math.pow(feat1[i] - feat2[i], 2)
    dist = 1 - math.pow(math.e, -SVM_G * 10000 * dist)
    return dist


def extract_data(ofname, maxclass):
    global d

    trainnames, testnames = get_list(d)
    trainnames = [name for tname in trainnames for name in tname]
    testnames = [name for tname in testnames for name in tname]

    max_size = 477000

    log("Extracting features...")

    traindata = np.empty((len(trainnames), max_size))
    trainlabels = np.array([])

    testdata = np.empty((len(testnames), max_size))
    testlabels = np.array([])


    try:
        count = 0
        intcount = 0
        for fname in trainnames:
            try:
                # log(fname)
                if ((count * 100)/len(trainnames) > (intcount + 1)): # unsure of this purpose
                    log("{}%... {}".format(intcount, fname))
                    intcount += 1
                (i, j) = str_to_sinste(fname) #i is the true site, j is the true inst
                if i == -1:
                    i = maxclass
                
                cells = load_cell(fname, ext='.csv')
                feats = extract(cells)

                trainlabels = np.append(trainlabels, i)
                new_arr = np.zeros_like(traindata[count])
                new_arr[:len(feats)] = feats
                traindata[count] = new_arr

                count += 1
            except:
                log("Failed to load trial:", fname)
                traceback.print_exc()
                pass


        log("Creating testing features...", len(testnames))


        count = 0
        intcount = 0
        for fname in testnames:
            try:
                # log(fname)
                if ((count * 100)/len(trainnames) > (intcount + 1)): # unsure of this purpose
                    log("{}%... {}".format(intcount, fname))
                    intcount += 1
                (i, j) = str_to_sinste(fname) #i is the true site, j is the true inst
                if i == -1:
                    i = maxclass
                cells = load_cell(fname, ext='.csv')
                feats = extract(cells)

                testlabels = np.append(testlabels, i)
                new_arr = np.zeros_like(testdata[count])
                new_arr[:len(feats)] = feats
                testdata[count] = new_arr

                count += 1
            except:
                log("Failed to load trial:", fname)
                pass


    except Exception as e:
        log('except in extract in mem')
        log('error:', e)
        traceback.print_exc()


    return trainlabels, traindata, testlabels, testdata





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

    print(conf_matrix)
    return conf_matrix # conf_matrix.tobytes().decode('utf-8')


def GenerateResults(guesses, answers):

    num_classes = len(np.unique(answers))

    correct_guesses = np.array(guesses == answers)
    incorrect_guesses = np.array(correct_guesses == False)

    # Print the stats
    log('\n')

    for i in range(0, num_classes):
        log(f'Accuracy for class {i}:', AccuracyForClass(i, guesses, answers))

    log('\n')

    for i in range(0, num_classes):
        log(f'Precision for class {i}:', PrecisionForClass(i, guesses, answers))

    log('\n')

    for i in range(0, num_classes):
        log(f'Recall for class {i}:', RecallForClass(i, guesses, answers))

    log('\n')

    for i in range(0, num_classes):
        log(f'F1 for class {i}:', F1ForClass(i, guesses, answers))

    log('\n')

    log(GenerateConfMatrix(guesses, answers, num_classes))
    log('vertical is what was actually guessed')



def main():
    global d
    # Load options
    try:
        optfname = sys.argv[1]
        d = load_options(optfname)
    except Exception as e:
        print(sys.argv[0], str(e))
        print("Perhaps you forgot to specify an options file?")
        sys.exit(0)


    # Print debug info
    print(sys.argv[0] + " " + sys.argv[1])
    print(repr(d))


    # Create output loc if necessary
    of = d["OUTPUT_LOC"] + '/c' + str(d["CLOSED_SITENUM"]) + '-i' + str(d["CLOSED_INSTNUM"]) + '-o' + str(d["OPEN_SITENUM"]) + '-i' + str(d["OPEN_INSTNUM"])

    if not os.path.exists(d["OUTPUT_LOC"]):
        os.mkdir(d["OUTPUT_LOC"])
    if not os.path.exists(of):
        os.mkdir(of)


    # Do some logging
    log(sys.argv[0] + " " + sys.argv[1])
    log(repr(d))


    ofname = of + '/data' # + sys.argv[0]


    trainlabels, traindata, testlabels, testdata = extract_data(ofname, d["CLOSED_SITENUM"])


    rbf = svm.SVC(kernel='rbf', gamma=0.5, C=0.1).fit(traindata, trainlabels)
    poly = svm.SVC(kernel='poly', degree=3, C=1).fit(traindata, trainlabels)


    # # This section is reading the predictions and getting things like TPR and FPR from them
    # guesses = np.array([ int(x.strip()) for x in open(confname, "r").readlines() ])
    # answers = np.array([ int(x.strip().split(' ')[0]) for x in open(testext, "r").readlines() ])


    # GenerateResults(guesses, answers)


if __name__ == '__main__':
    main()

