#!/bin/python3
import subprocess
import math
import sys
import time
from loaders import *
import numpy as np, traceback
from sklearn import svm
# from gen_list import *


#np.set_logoptions(threshold=np.inf)

# np.seterr(invalid='raise')
np.set_printoptions(threshold=np.inf)


d = {}

def flog(msg, fname):
    f = open(fname, "a+")
    f.write(str(msg) + "\n")
    f.close()    


def log(*args):
    global d
    msg = ' '.join(map(str, args))
    print(msg)
    LOG_FILE = d["OUTPUT_LOC"] + '/' + 'c' + str(d["CLOSED_SITENUM"]) + '-i' + str(d["CLOSED_INSTNUM"]) + '-o' + str(d["OPEN_SITENUM"]) + '-i' + str(d["OPEN_INSTNUM"]) + '/' + 'log.txt'
    flog(msg, LOG_FILE)


"""
    Please implement this. Use sizes as y and times as x
        then do the prediction
"""
def size_extract(sinste, interpolants = 1000):
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


def extract(sinste, num_points = 1000):
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

    global d
    LOG_FILE = d["OUTPUT_LOC"] + '/' + 'c' + str(d["CLOSED_SITENUM"]) + '-i' + str(d["CLOSED_INSTNUM"]) + '-o' + str(d["OPEN_SITENUM"]) + '-i' + str(d["OPEN_INSTNUM"]) + '/' + 'guesses-and-answers.txt'

    fd = open(LOG_FILE, 'w')
    fd.write("guesses, answers\n")
    for i, el in enumerate(guesses):
        fd.write(str(el) + ',' + str(answers[i]) + "\n")




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
        print('answers[i]', answers[i], type(answers[i]))
        print('el', el, type(el))
        conf_matrix[int(answers[i]), int(el)] += 1

    return conf_matrix



def extract_data(ofname, maxclass):
    global d

    trainnames, testnames = get_list(d)
    trainnames = [name for tname in trainnames for name in tname]
    testnames = [name for tname in testnames for name in tname]

    max_size = 1003

    log("Extracting features...")

    traindata = np.empty((len(trainnames), max_size))
    trainlabels = np.ones(len(trainnames)) * -1

    testdata = np.empty((len(testnames), max_size))
    testlabels = np.ones(len(testnames)) * -1


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

                trainlabels[count] = i
                traindata[count] = feats

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
                if ((count * 100)/len(testnames) > (intcount + 1)): # unsure of this purpose
                    log("{}%... {}".format(intcount, fname))
                    intcount += 1
                (i, j) = str_to_sinste(fname) #i is the true site, j is the true inst
                if i == -1:
                    i = maxclass
                cells = load_cell(fname, ext='.csv')
                feats = extract(cells)

                testlabels[count] = i
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


    log('Logging rbf data')
    guesses = rbf.predict(testdata)
    GenerateResults(guesses, testlabels)

    log('Logging poly data')
    guesses = poly.predict(testdata)
    GenerateResults(guesses, testlabels)



if __name__ == '__main__':
    main()

 
