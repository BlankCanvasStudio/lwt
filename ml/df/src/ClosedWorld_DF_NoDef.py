#!/bin/python3
# -*- coding: utf-8 -*-

# This code is to implement deep fingerloging model for website fingerloging attacks
# ACM Reference Formant
# Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. 2018.
# Deep Fingerloging: Undermining Website Fingerloging Defenses with Deep Learning.
# In 2018 ACM SIGSAC Conference on Computer and Communications Security (CCS ’18),
# October 15–19, 2018, Toronto, ON, Canada. ACM, New York, NY, USA, 16 pages.
# https://doi.org/10.1145/3243734.3243768


from keras import backend as K
from keras.models import load_model
from utility import LoadDataNoDefCW
from Model_NoDef import DFNet
import random
# from keras.utils import np_utils
# from tensorflow.keras.utils import np_utils
from tensorflow.keras.utils import to_categorical
# from keras.optimizers import Adamax
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers.schedules import ExponentialDecay
import numpy as np
import os, math

np.set_printoptions(threshold=np.inf)

def flog(msg, fname):
    f = open(fname, "a+")
    f.write(str(msg) + "\n")
    f.close()

def log(*args):
    global num_inst
    global num_classes
    msg = ' '.join(map(str, args))
    print(msg)
    LOG_FILE = './results/c' + str(num_classes) + '-i' + str(num_inst) + '/log.txt'
    flog(msg, LOG_FILE)

def GenerateResults(guesses, answers):

    # num_classes = len(np.unique(answers))
    # num_classes = (np.max(answers))

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

    log(GenerateConfMatrix(guesses, answers))
    log('vertical is what was actually guessed')




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
def GenerateConfMatrix(guesses, answers):
    print('num classes:', num_classes)
    print('unqiue:',len(np.unique(answers)))
    print('answers:', answers)
    print(sorted(list(set(answers))))
    conf_matrix = np.zeros((num_classes, num_classes))

    for i, el in enumerate(guesses):
        print(answers[i], el)
        conf_matrix[answers[i], el] += 1

    return conf_matrix




random.seed(0)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'



# Use only CPU
#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
#os.environ["CUDA_VISIBLE_DEVICES"] = ""

description = "Training and evaluating DF model for closed-world scenario on non-defended dataset"

print(description)
# Training the DF model
NB_EPOCH = 30   # Number of training epoch
print("Number of Epoch: ", NB_EPOCH)
BATCH_SIZE = 128 # Batch size
VERBOSE = 2 # Output display mode
LENGTH = 10000 # Packet sequence length
# OPTIMIZER = Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0) # Optimizer

# Define a learning rate schedule
lr_schedule = ExponentialDecay(
    initial_learning_rate=0.002,
    decay_steps=10000,
    decay_rate=0.9)

# Use the learning rate schedule in the optimizer
OPTIMIZER = Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=1e-08)


NB_CLASSES = 95 # number of outputs = number of classes
INPUT_SHAPE = (LENGTH,1)


# Data: shuffled and split between train and test sets
print("Loading and preparing data for training, and evaluating the model")
X_train, y_train, X_valid, y_valid, X_test, y_test = LoadDataNoDefCW(length=LENGTH)
# Please refer to the dataset format in readme
# K.set_image_dim_ordering("tf") # tf is tensorflow
K.set_image_data_format("channels_last") # tf is tensorflow

# Convert data as float32 type
X_train = X_train.astype('float32')
X_valid = X_valid.astype('float32')
X_test = X_test.astype('float32')
y_train = y_train.astype('float32')
y_valid = y_valid.astype('float32')
y_test = y_test.astype('float32')


num_classes = len(np.unique(y_train))
num_inst = math.ceil((X_train.shape[0] + X_valid.shape[0] + X_test.shape[0]) / num_classes)
 
if not os.path.exists('./results'):
    os.mkdir('./results')

if not os.path.exists('./results/c' + str(num_classes) + '-i' + str(num_inst)):
    os.mkdir('./results/c' + str(num_classes) + '-i' + str(num_inst))



# we need a [Length x 1] x n shape as input to the DF CNN (Tensorflow)
X_train = X_train[:, :,np.newaxis]
X_valid = X_valid[:, :,np.newaxis]
X_test = X_test[:, :,np.newaxis]

log(X_train.shape[0], 'train samples')
log(X_valid.shape[0], 'validation samples')
log(X_test.shape[0], 'test samples')

# Convert class vectors to categorical classes matrices
y_train = to_categorical(y_train, NB_CLASSES)
y_valid = to_categorical(y_valid, NB_CLASSES)
y_test = to_categorical(y_test, NB_CLASSES)

# Building and training model
log ("Building and training DF model")

model = DFNet.build(input_shape=INPUT_SHAPE, classes=NB_CLASSES)

model.compile(loss="categorical_crossentropy", optimizer=OPTIMIZER,
	metrics=["accuracy"])
log ("Model compiled")

# # Start training
history = model.fit(X_train, y_train,
        batch_size=BATCH_SIZE, epochs=NB_EPOCH,
        verbose=VERBOSE, validation_data=(X_valid, y_valid))

model_filepath = './results/c' + str(num_classes) + '-i' + str(num_inst) + '/output.model'


model.save(model_filepath)
del model
model = load_model(model_filepath)

probs = model.predict(X_test)
log('probs:', probs)
guesses = [ np.argmax(x) for x in probs ]
y_test_decoded = np.argmax(y_test, axis=1)
log('guesses:', guesses)
log('y_test:', y_test_decoded)
GenerateResults(guesses, y_test_decoded)

