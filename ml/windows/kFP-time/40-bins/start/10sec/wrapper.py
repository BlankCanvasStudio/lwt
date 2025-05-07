#!/bin/python3 
from multiprocessing import Pool
import pdb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from multiprocessing import Semaphore # Lock
from multiprocessing import Lock
from multiprocessing import set_start_method, get_context
import csv
import sys, struct, traceback
import math
from sys import stdout
import numpy as np
import operator, sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn import tree
import sklearn.metrics as skm
import scipy
import dill
import random
import os
from collections import defaultdict
import argparse
from itertools import chain
from loaders import *
import subprocess
import numpy as np
import traceback
from sklearn.inspection import permutation_importance
from locator import find_start_of_data
# from guppy import hpy

d = {}

def flog(msg, fname):
    f = open(fname, "a+")
    f.write(str(msg) + "\n")
    f.close()    

def log(*args):
    global max_class_global
    global inst_global
    msg = ' '.join(map(str, args))
    print(msg)
    LOG_FILE = d["OUTPUT_LOC"] + '/' + 'c' + str(d["CLOSED_SITENUM"]) + '-i' + str(d["CLOSED_INSTNUM"]) + '-o' + str(d["OPEN_SITENUM"]) + '-i' + str(d["OPEN_INSTNUM"]) + '/' + 'log.txt'
    flog(msg, LOG_FILE)

np.seterr(invalid='raise')
np.set_printoptions(threshold=np.inf)

#1. dictionary_() will extract features and write them to a target file (kFPdict) in the data folder
#2. calls RF_openworld(), which starts by dividing kFPdict into training and testing sets
#3. # -1 is IN, 1 is OUT
#file format: "direction time size"

"""Feeder functions"""

def neighborhood(iterable):
    iterator = iter(iterable)
    prev = (0)
    item = next(iterator)  # throws StopIteration if empty.
    for nex in iterator:
        yield (prev,item,nex)
        prev = item
        item = nex
    yield (prev,item,None)

def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0
  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg
  return out

"""Non-feeder functions"""


def get_pkt_list(fname, start_time, duration):
    fd = open(fname, 'rb')
    # size, time
    sequence = []

    fd.seek(4)
    offset = struct.unpack('d', fd.read(8))[0]
    file_size = os.path.getsize(fname)

    length = (file_size // 12) # 4 for int and 8 for double
    [ times, direction ] = [ np.zeros(length, dtype=np.float64), np.ones(length, dtype=int) ]

    index = 0
    while fd.tell() < file_size:
        size = int.from_bytes(fd.read(4), sys.byteorder)
        time = struct.unpack('d', fd.read(8))[0]

        zerod_time = time - offset
        if zerod_time >= 0 and zerod_time >= start_time and zerod_time < start_time + duration:
            times[index] = time - offset

            index += 1

    fd.close()

    # Remove all values outside the int range
    mask = (times < -sys.maxsize - 1) | (times > sys.maxsize)
    # Convert values outside the range to zero
    times[mask] = 0


    return np.array(list(zip(times[:index + 1], direction[:index + 1])))


def In_Out(list_data):
    In = list_data[list_data[:, 1] == -1]
    Out = list_data[list_data[:, 1] == 1]
    return In, Out



############### TIME FEATURES #####################

def inter_pkt_time(list_data):
    return list_data[:-1, 0] - list_data[1:, 0]



def interarrival_times(In, Out, Total): # (list_data):
    IN = inter_pkt_time(In)
    OUT = inter_pkt_time(Out)
    TOTAL = inter_pkt_time(Total)
    return IN, OUT, TOTAL


def interarrival_maxminmeansd_stats(In, Out, Total):# (list_data):
    interstats = []
    In, Out, Total = interarrival_times(In, Out, Total)
    avg_out = np.sum(Out)/float(len(Out))
    avg_total = np.sum(Total)/float(len(Total))
    interstats.append((np.max(Out), np.max(Total), avg_out, avg_total, np.std(Out), np.std(Total), np.percentile(Out, 75), np.percentile(Total, 75)))
    return interstats

def time_percentile_stats(In, Out, Total):
    Out1 = Out[:, 0]
    Total1 = Total[:, 0]
    STATS = []
    if len(Out1):
        STATS.append(np.percentile(Out1, 25)) # return 25th percentile
        STATS.append(np.percentile(Out1, 50))
        STATS.append(np.percentile(Out1, 75))
        STATS.append(np.percentile(Out1, 100))
    if not len(Out1):
        STATS.extend(([0]*4))
    if len(Total1):
        STATS.append(np.percentile(Total1, 25)) # return 25th percentile
        STATS.append(np.percentile(Total1, 50))
        STATS.append(np.percentile(Total1, 75))
        STATS.append(np.percentile(Total1, 100))
    if not len(Total1):
        STATS.extend(([0]*4))
    return STATS

def number_pkt_stats(In, Out, Total):
    return len(Out), len(Total)

 
def first_and_last_30_pkts_stats(Total):

    first30in = Total[np.where(Total[:30,1] == -1), 0]
    first30out = Total[np.where(Total[:30,1] == 1), 0]
    last30in = Total[np.where(Total[-30:,1] == -1), 0]
    last30out = Total[np.where(Total[-30:,1] == 1), 0]

    stats= []
    stats.append(len(first30in))
    stats.append(len(first30out))
    stats.append(len(last30in))
    stats.append(len(last30out))
    return stats

#concentration of outgoing packets in chunks of 20 packets
def pkt_concentration_stats(Total):
    chunks = Total.reshape(1, -20)
    concentrations = np.empty(len(chunks))
    for i in range(len(chunks)):
        c = np.count_nonzero(chunks[i][1] == 1)
        concentrations[i] = c
    return  concentrations

#Average number packets sent and received per second
def make_bins(Total):
    counts, bin_edges = np.histogram(Total[:,0], bins = 40)
    return counts


#Variant of packet ordering features from http://cacr.uwaterloo.ca/techreports/2014/cacr2014-05.pdf
def avg_pkt_ordering_stats(Total):

    # Total = get_pkt_list(trace_data)
    temp1 = np.where(Total[:,1] == 1)[0]


    avg_in = np.sum(temp1)/float(len(temp1)) if len(temp1) else 0

    if len(temp1):
        std1 = np.std(temp1)
    else:
        std1 = 0

    return avg_in, std1



def perc_inc_out(In, Out, Total):
    percentage_in = len(In)/float(len(Total))
    percentage_out = len(Out)/float(len(Total))
    return percentage_in, percentage_out


############### FEATURE FUNCTION #####################


#If size information available add them in to function below
def TOTAL_FEATURES(trace_data, max_size=175): # tracedata is now a filename but to lazy to copy and paste yet

    start_time = find_start_of_data(trace_data)

    # Duration is in sec
    Total = get_pkt_list(trace_data, start_time, duration = 10)

    bin_counts = make_bins(Total) # 6 long

    running_list = 1

    ALL_FEATURES = bin_counts
    # log('per sec raw:', running_list, '-', running_list + (len(bin_counts) if hasattr(bin_counts, '__len__') else 1) - 1)
    # running_list += len(bin_counts) if hasattr(bin_counts, '__len__') else 1

    while len(ALL_FEATURES)<max_size:
        ALL_FEATURES = np.append(ALL_FEATURES, 0)
    features = ALL_FEATURES[:max_size]

    return tuple(features)


def chunks(l, n):
    """ Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def checkequal(lst):
    return lst[1:] == lst[:-1]


############ Non-Feeder functions ########

def extract_dill(args):
    '''Extract Features -- A dictionary containing features for each traffic instance.'''

    [ trainnames, testnames, ofname, maxclass ] = args

    try:
        os.remove(ofname + '-train.txt')
        os.remove(ofname + '-test.txt')
    except:
        pass


    try:

        log("Creating training features...", len(trainnames))

        # maxclass = num_classes + 1
        #for kFP, we write the final class not as -1, but as maxclass
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
                
                output_array = TOTAL_FEATURES(fname)
                print('first data array:', output_array[0])
                output_array = np.append(i, output_array)

                with open(ofname + '-train.txt', 'a') as f:
                    f.write(np.array2string(output_array, separator=',').replace('\n', '')[1:-1] + '\n')
                del output_array
                count += 1
            except:
                log("Failed to load trial:", fname)
                pass

        log("Creating testing features...", len(testnames))

        count = 0
        intcount = 0
        for fname in testnames:
            try:
                # log(fname)
                if ((count * 100)/len(testnames) > (intcount + 1)):
                    log("{}%... {}".format(intcount, fname))
                    intcount += 1
                (i, j) = str_to_sinste(fname) #i is the true site, j is the true inst
                if i == -1:
                    i = maxclass

                output_array = TOTAL_FEATURES(fname)
                output_array = np.append(i, output_array)

                with open(ofname + '-test.txt', 'a') as f:
                    f.write(np.array2string(output_array, separator=',').replace('\n', '')[1:-1] + '\n')
                del output_array
                count += 1
            except:
                log("Failed to load trial:", fname)
                pass


    except Exception as e:
        log('except in extract_dill')
        log('error:', e)
        log(traceback.print_exc())

    return


def in_mem_extract(ofname, max_class):
    '''Extract Features -- A dictionary containing features for each traffic instance.'''

    atrainnames, atestnames = get_list(d)
    #unpack trainnames, testnames
    trainnames = [name for tname in atrainnames for name in tname]
    testnames = [name for tname in atestnames for name in tname]

    max_size = 175

    traindata = np.empty((len(trainnames), max_size - 1))
    trainlabels = np.zeros(len(trainnames))

    testdata = np.empty((len(testnames), max_size - 1))
    testlabels = np.zeros(len(testnames))

    try:

        log("Creating training features...", len(trainnames))

        # maxclass = num_classes + 1
        #for kFP, we write the final class not as -1, but as maxclass
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
                    i = max_class
                
                output_array = TOTAL_FEATURES(fname, max_size = max_size)[1:]
                # print('first amount:', output_array[0], output_array[1])

                trainlabels[count] = i
                traindata[count] = output_array

                count += 1
            except:
                log("Failed to load trial:", fname)
                log(traceback.print_exc())
                pass

        log("Creating testing features...", len(testnames))

        count = 0
        intcount = 0
        for fname in testnames:
            try:
                # log(fname)
                if ((count * 100)/len(testnames) > (intcount + 1)): # unsure of this purpose
                    log("{}%... {}".format(intcount, fname))
                    intcount += 1
                (i, j) = str_to_sinste(fname) #i is the true site, j is the true inst
                if i == -1:
                    i = max_class
                
                output_array = TOTAL_FEATURES(fname, max_size = max_size)[1:]

                testlabels[count] = i
                testdata[count] = output_array

                count += 1
            except:
                log("Failed to load trial:", fname)
                log(traceback.print_exc())
                pass

    except Exception as e:
        log('except in extract in mem')
        log('error:', e)
        log(traceback.print_exc())
    

    return trainlabels, traindata, testlabels, testdata



def RF_openworld(testnames, ofname, max_class):
    '''Produces leaf vectors used for classification.'''

    trainlabel = np.array([])
    testlabel  = np.array([])

    traindata =  []
    testdata  =  []

    if not ("IN_MEM" in d and d["IN_MEM"] == 1):

        for line in open(ofname + '-train.txt', 'r'):
            line = line.replace(' ', '')
            arr = np.fromstring(line, dtype=float, sep=',')

            trainlabel = np.append(trainlabel, arr[0])
            traindata.append( arr[1:] )

        for line in open(ofname + '-test.txt', 'r'):
            line = line.replace(' ', '')
            arr = np.fromstring(line, dtype=float, sep=',')

            testlabel = np.append(testlabel, arr[0])
            testdata.append( arr[1:] )

        traindata =  np.array(traindata)
        testdata  =  np.array(testdata)

    else:

        trainlabel, traindata, testlabel, testdata = in_mem_extract(ofname, max_class)




    if len(traindata) != len(trainlabel):
        log("Unexpected train size: {} != {}".format(len(traindata), len(trainlabel)))
        raise("Unexpected train size: {} != {}".format(len(traindata), len(trainlabel)))

   
    log("Training ...")
    model = RandomForestClassifier(n_jobs=-1, n_estimators=1000, oob_score=True)
    # model = tree.DecisionTreeRegressor(max_depth=100)

    model.fit(traindata, trainlabel)


    #taow: read names from relevant test list
    if len(testdata) != len(testlabel):
        log("Unexpected test size: {} != {}".format(len(testdata), len(testlabel)))
        raise("Unexpected test size: {} != {}".format(len(testdata), len(testlabel)))

    M = model.predict(testdata)

    probs = model.predict_proba(testdata)

    return M, testlabel, probs, model, testdata


def GenerateResults(guesses, answers, probs, forest, x_test):

    global d

    LOG_FILE = d["OUTPUT_LOC"] + '/' + 'c' + str(d["CLOSED_SITENUM"]) + '-i' + str(d["CLOSED_INSTNUM"]) + '-o' + str(d["OPEN_SITENUM"]) + '-i' + str(d["OPEN_INSTNUM"]) + '/' + 'guesses-and-answers.txt'

    fd = open(LOG_FILE, 'w')
    fd.write("guesses, answers\n")
    for i, el in enumerate(guesses):
        fd.write(str(answers[i]) + ',' + ','.join([ str(x) for x in probs[i] ]) +  '\n')
        # fd.write(str(el) + ',' + str(answers[i]) + "\n")
    fd.close()

    num_classes = d["CLOSED_SITENUM"] + 1 # len(np.unique(answers))

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

    log('\n')

    log('Generating Feature Importance')
    log(GenerateImportantFeatures(forest, x_test, answers))

    log('\n')


def GenerateImportantFeatures(forest, x_test, y_test):
    log('\n')
    log('feature_importances_ based on mean decrease in impurity')
    log(forest.feature_importances_)

    log('\n')
    log('finding permutation importance')
    log(permutation_importance(
        forest, x_test, y_test, n_repeats=10, random_state=42, n_jobs=2
        ))



def TP(c, correct_guesses, answers):
    return np.count_nonzero(correct_guesses[answers == c])

def FP(c, incorrect_guesses, guesses):
    return np.count_nonzero(incorrect_guesses[guesses == c])

def FN(c, incorrect_guesses, answers):
    return  np.count_nonzero(incorrect_guesses[answers == c])

def TN(c, correct_guesses, answers):
    return np.count_nonzero(correct_guesses[answer != c])


# Accuracy, precision, recall, f1, and aoc_roc

# Acc = # correct / Total #
def AccuracyForClass(c, guesses, answers):

    correct_guesses = np.array(guesses == answers)

    denom = np.count_nonzero(guesses == c)
    if not denom: return -1
    return TP(c, correct_guesses, answers) / denom



# Precision = TP / (TP + FP). This is per class
def PrecisionForClass(c, guesses, answers):

    correct_guesses = np.array(guesses == answers)
    incorrect_guesses = np.array(correct_guesses == False)

    denom = (TP(c, correct_guesses, answers) + FP(c, incorrect_guesses, guesses))
    if not denom: return -1
    return TP(c, correct_guesses, answers) / denom



# Recall = TP / (TP + FN). This is per class
def RecallForClass(c, guesses, answers):

    correct_guesses = np.array(guesses == answers)
    incorrect_guesses = np.array(correct_guesses == False)

    denom = (TP(c, correct_guesses, answers) + FN(c, incorrect_guesses, answers))
    if not denom: return -1
    return TP(c, correct_guesses, answers) / denom



# F1 = 2 (Precision * Recall) / (Precision + Recall). This is per class
def F1ForClass(c, guesses, answers):
    denom =  (PrecisionForClass(c, guesses, answers) + RecallForClass(c, guesses, answers))
    if not denom: return -1
    return 2 * (PrecisionForClass(c, guesses, answers) * RecallForClass(c, guesses, answers)) / denom



# Just helpful for me to visualize
def GenerateConfMatrix(guesses, answers, num_classes):
    conf_matrix = np.zeros((num_classes, num_classes))

    for i, el in enumerate(guesses):
        print(int(answers[i]), int(el))
        conf_matrix[int(answers[i]), int(el)] += 1

    return conf_matrix


def main():
    try:
        optfname = sys.argv[1] if sys.argv[1] else 'options.txt'
        global d
        d = load_options(optfname)
    except:
        log(sys.argv[0], sys.exc_info()[0])
        sys.exit(0)

    try:

        of = d["OUTPUT_LOC"] + '/c' + str(d["CLOSED_SITENUM"]) + '-i' + str(d["CLOSED_INSTNUM"]) + '-o' + str(d["OPEN_SITENUM"]) + '-i' + str(d["OPEN_INSTNUM"])
        ofname = of + '/data' # + sys.argv[0]

        if not os.path.exists(d["OUTPUT_LOC"]):
            os.mkdir(d["OUTPUT_LOC"])

        if not os.path.exists(of):
            os.mkdir(of)


        atrainnames, atestnames = get_list(d)
        #unpack trainnames, testnames
        trainnames = [name for tname in atrainnames for name in tname]
        testnames = [name for tname in atestnames for name in tname]

        if ("DO_NOT_EXTRACT" not in d or d["DO_NOT_EXTRACT"] != 1) and \
                not ("IN_MEM" in d and d["IN_MEM"] == 1):
            extract_dill([trainnames, testnames, ofname, d["CLOSED_SITENUM"]])

        M, testlabel, probs, forest, x_test = RF_openworld(testnames, ofname, d["CLOSED_SITENUM"]) #testnames is only used to output score here

        GenerateResults(M, testlabel, probs, forest, x_test)

    except Exception as e:
        traceback.print_exc()
        log(e)
        log(traceback.print_exc())

if __name__ == '__main__':
    main()

