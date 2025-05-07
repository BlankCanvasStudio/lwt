#!/bin/python3
import subprocess
import math
import sys
import time
from loaders import *
import numpy as np
# from gen_list import *


np.set_printoptions(threshold=np.inf)

d = {}

##for c_i in range(0, 10):
##    for g_i in range(0, 10):
##        cpow = (c_i - 5) * 2
##        gpow = (g_i - 5) * 2
##        c = math.pow(10, cpow)
##        g = math.pow(10, gpow)
##        cmd = "./svm-train "
##        cmd += "-c " + str(c) + " "
##        cmd += "-g " + str(g) + " "
##        cmd += "svm.train svm.model"
##        subprocess.call(cmd, shell=True)
##
##        cmd = "./svm-predict svm.test svm.model svm.results >> temp-acc"
##        subprocess.call(cmd, shell=True)
##
##        cmd = "grep Accuracy temp-acc"
##        s = subprocess.check_output(cmd, shell=True)
##        log(c_i, g_i, c, g, s)
##
##        cmd = "rm svm.results"
##        cmd = "rm temp-acc"
##        subprocess.call(cmd, shell=True)

def flog(msg, fname):
    f = open(fname, "a+")
    f.write(str(msg) + "\n")
    f.close()    

def log(*args):
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



    # #input "sinste" is a list of cells
    # features = []
    # 
    # #SIZE MARKERS
    # #does not do anything for cells; see number markers
    # mcount = 0 #number of markers, pad to 300 later
    # sizemarker = 0 #size accumulator
    # for si in range(0, len(sinste)):
    #     if (si > 0):
    #         if (sinste[si] * sinste[si-1] < 0): # direction change
    #             features.append(sizemarker/600)
    #             mcount += 1
    #     sizemarker += sinste[si] #can be negative
    #     if mcount >= 300:
    #         break

    # for i in range(mcount, 300):
    #     features.append(0)



    # # Could use our approx here

    # #HTML SIZE
    # #this almost certainly doesn't actually give html document size
    # count_started = 0
    # htmlsize = 0
    # appended = 0
    # for si in range(0, len(sinste)):
    #     if sinste[si] < 0: #incoming
    #         count_started = 1
    #         htmlsize += sinste[si]
    #     if sinste[si] > 0 and count_started == 1:
    #         features.append(htmlsize)
    #         appended = 1
    #         break
    # if (appended == 0):
    #     features.append(0)

    # #TOTAL TRANSMITTED BYTES
    # totals = [0, 0]
    # for si in range(0, len(sinste)):
    #     if (sinste[si] < 0):
    #         totals[0] += abs(sinste[si])
    #     if (sinste[si] > 0):
    #         totals[1] += abs(sinste[si])
    # features.append(totals[0])
    # features.append(totals[1])

    # #NUMBER MARKERS
    # mcount = 0 #also 300
    # nummarker = 0
    # for si in range(0, len(sinste)):
    #     if (si > 0):
    #         if (sinste[si] * sinste[si-1] < 0): # direction change
    #             features.append(nummarker)
    #             mcount += 1
    #     nummarker += 1
    #     if mcount >= 300:
    #         break

    # for i in range(mcount, 300):
    #     features.append(0)

    # #NUM OF UNIQUE PACKET SIZES
    # uniqsizes = []
    # for si in range(0, len(sinste)):
    #     if not(sinste[si] in uniqsizes):
    #         uniqsizes.append(sinste[si])
    # features.append(len(uniqsizes)/2) #just 1 for cells

    # #PERCENTAGE INCOMING PACKETS
    # if sum(totals) != 0:
    #     t = totals[0]/float(sum(totals))
    #     t = int(t/0.05) * 0.05 #discretize by 0.05
    #     features.append(t)
    # else:
    #     features.append(0)

    # #NUMBER OF PACKETS
    # t = totals[0] + totals[1]
    # t = int(t/15) * 15 #discertize by 15
    # features.append(t)

    # for si in range(0, len(sinste)):
    #     features.append(sinste[si])

    # return features



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

try:
    optfname = sys.argv[1]
    d = load_options(optfname)
except Exception as e:
    print(sys.argv[0], str(e))
    print("Perhaps you forgot to specify an options file?")
    sys.exit(0)


print(sys.argv[0] + " " + sys.argv[1])
print(repr(d))


of = d["OUTPUT_LOC"] + '/c' + str(d["CLOSED_SITENUM"]) + '-i' + str(d["CLOSED_INSTNUM"]) + '-o' + str(d["OPEN_SITENUM"]) + '-i' + str(d["OPEN_INSTNUM"])

if not os.path.exists(d["OUTPUT_LOC"]):
    os.mkdir(d["OUTPUT_LOC"])

if not os.path.exists(of):
    os.mkdir(of)


# Do some logging
log(sys.argv[0] + " " + sys.argv[1])
log(repr(d))

[ tpc, tnc, nc, pc ] = [ 0, 0, 0, 0 ]

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

    for type_i in range(0, 2):
        fout = open(fullexts[type_i], "w")
        for ci in range(0, len(fullnames[type_i])):
            log("Site {} of {}".format(ci, len(fullnames[type_i])))
            for ti in range(0, len(fullnames[type_i][ci])):
                try:
                    cells = load_cell(fullnames[type_i][ci][ti], ext='.csv')
                    feats = extract(cells)
                    fout.write(str(ci))
                    for fi in range(0, len(feats)):
                        fout.write(" " + str(fi+1) + ":" + str(feats[fi]))
                    fout.write("\n")
                except:
                    log("Failed loading data for:", fullnames[type_i][ci][ti])
                    pass
        fout.close()


if not("SVM_C_LOG" in d and "SVM_G_LOG" in d):
    d["SVM_C_LOG"] = 10
    d["SVM_G_LOG"] = -25
SVM_C = math.pow(2.0, d["SVM_C_LOG"])
SVM_G = math.pow(2.0, d["SVM_G_LOG"])


log("Start training...")
# cmd = "./svm-train -c {} -g {} {} {}".format(
#     SVM_C, SVM_G, trainext, modelext)
cmd = "../libsvm/svm-train -c {1} -g {2} {3} {0}.model".format(
    ofname, SVM_C, SVM_G, trainext)
subprocess.call(cmd, shell=True)
    

# cmd = "./svm-predict -o {} {} {} {}.svmlog".format(
#     confname, testext, modelext, ofname)
# subprocess.call(cmd, shell=True)
log("Start testing...")
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

    print(conf_matrix)
    return conf_matrix # conf_matrix.tobytes().decode('utf-8')

# Print the stats
log('\n')

for i in range(0, num_classes):
    log('Accuracy for class ', i, ':', AccuracyForClass(i))

log('\n')

for i in range(0, num_classes):
    log('Precision for class', i, ':', PrecisionForClass(i))

log('\n')

for i in range(0, num_classes):
    log('Recall for class', i, ':', RecallForClass(i))

log('\n')

for i in range(0, num_classes):
    log('F1for class', i, ':', F1ForClass(i))

log('\n')

log(GenerateConfMatrix())
log('vertical is what was actually guessed')

