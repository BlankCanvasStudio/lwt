#!/bin/python3
from keras import backend as K
from keras.models import Sequential, load_model
from keras.layers import Conv1D, MaxPooling1D, BatchNormalization
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.initializers import glorot_uniform
from keras.callbacks import ModelCheckpoint, EarlyStopping
import random
from keras.utils import to_categorical
# from keras.optimizers import Adam
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers.schedules import ExponentialDecay
import numpy as np
import sys
import os
from timeit import default_timer as timer
#from plog import plog
import argparse
import json, math
from data_utils import *

random.seed(0)
np.set_printoptions(threshold=np.inf)


max_class_global = 0
inst_global = 0
model_file = ''
processing = 'none'


def flog(msg, fname):
    f = open(fname, "a+")
    f.write(str(msg) + "\n")
    f.close()    

input_size = 500000
def log(*args):
    global max_class_global
    global inst_global
    global processing
    msg = ' '.join(map(str, args))
    print(msg)
    LOG_FILE = './results/c' + str(max_class_global) + '-i' + str(inst_global) + processing + '/log.txt'
    flog(msg, LOG_FILE)


# de the ConvNet
class ConvNet:
    @staticmethod
    def build(classes,
              input_shape,
              activation_function=("elu", "relu", "relu", "relu", "relu", "relu"),
              dropout=(0.1, 0.1, 0.1, 0.1, 0.5, 0.7),
              filter_num=(32, 64, 128, 256),
              kernel_size=8,
              conv_stride_size=1,
              pool_stride_size=4,
              pool_size=8,
              fc_layer_size=(512, 512)):

        # confirm that parameter vectors are acceptable lengths
        assert len(filter_num) + len(fc_layer_size) <= len(activation_function)
        assert len(filter_num) + len(fc_layer_size) <= len(dropout)

        # Sequential Keras model template
        model = Sequential()

        # add convolutional layer blocks
        for block_no in range(0, len(filter_num)):
            if block_no == 0:
                model.add(Conv1D(filters=filter_num[block_no],
                                 kernel_size=kernel_size,
                                 input_shape=input_shape,
                                 strides=conv_stride_size,
                                 padding='same',
                                 name='block{}_conv1'.format(block_no)))
            else:
                model.add(Conv1D(filters=filter_num[block_no],
                                 kernel_size=kernel_size,
                                 strides=conv_stride_size,
                                 padding='same',
                                 name='block{}_conv1'.format(block_no)))

            model.add(BatchNormalization())

            model.add(Activation(activation_function[block_no], name='block{}_act1'.format(block_no)))

            model.add(Conv1D(filters=filter_num[block_no],
                             kernel_size=kernel_size,
                             strides=conv_stride_size,
                             padding='same',
                             name='block{}_conv2'.format(block_no)))

            model.add(BatchNormalization())

            model.add(Activation(activation_function[block_no], name='block{}_act2'.format(block_no)))

            model.add(MaxPooling1D(pool_size=pool_size,
                                   strides=pool_stride_size,
                                   padding='same',
                                   name='block{}_pool'.format(block_no)))

            model.add(Dropout(dropout[block_no], name='block{}_dropout'.format(block_no)))

        # flatten output before fc layers
        model.add(Flatten(name='flatten'))

        # add fully-connected layers
        for layer_no in range(0, len(fc_layer_size)):
            model.add(Dense(fc_layer_size[layer_no],
                            kernel_initializer=glorot_uniform(seed=0),
                            name='fc{}'.format(layer_no)))

            model.add(BatchNormalization())
            model.add(Activation(activation_function[len(filter_num)+layer_no],
                                 name='fc{}_act'.format(layer_no)))

            model.add(Dropout(dropout[len(filter_num)+layer_no],
                              name='fc{}_drop'.format(layer_no)))

        # add final classification layer
        model.add(Dense(classes, kernel_initializer=glorot_uniform(seed=0), name='fc_final'))
        model.add(Activation('softmax', name="softmax"))

        # compile model with Adamax optimizer
        # optimizer = Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
        # optimizer = Adam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

        lr_schedule = ExponentialDecay(
            initial_learning_rate=0.002,
            decay_steps=10000,
            decay_rate=0.9)

        # Use the learning rate schedule in the optimizer
        optimizer = Adam(learning_rate=lr_schedule, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

        model.compile(loss="categorical_crossentropy",
                      optimizer=optimizer,
                      metrics=["accuracy"])
        return model


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description='Train and test the DeepFingerloging model in the Closed-World setting.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--traces',
                        type=str,
                        required=True,
                        metavar='<path/to/traffic>',
                        help='Path to the directory where the traffic data is stored.')
    parser.add_argument('-a', '--attack',
                        type=int,
                        default=0,
                        metavar='<attack_type>',
                        help='Type of attack: (0) direction (1) tik-tok (2) timing')
    parser.add_argument('-o', '--output',
                        type=str,
                        default='trained_model_cw.h5',
                        metavar='<output>',
                        help='Location to store the file.')
    parser.add_argument('-f', '--folds',
                        type=int,
                        default=5,
                        metavar='<num_folds>',
                        help='Number of folds to use for cross-validation.')
    parser.add_argument('-p', '--processing',
                        type=str,
                        default='none',
                        metavar='<processing>',
                        help='How would you like the data processed before training. Options: none, approx-arrival')
    parser.add_argument('-l', '--length',
                        type=int,
                        default=5000,
                        metavar='<length>',
                        help='How long should the input to the neural net be?')
    return parser.parse_args()


def attack(X_train, y_train, X_valid, y_valid, X_test, y_test, args, VERBOSE=1):
    """
    """

    global max_class_global
    global inst_global

    # convert class vectors to binary class matrices
    classes = np.max(y_train) + 1
    print(set(list(y_train)))
    y_train = to_categorical(y_train, classes)
    y_valid = to_categorical(y_valid, classes)
    y_test = to_categorical(y_test, classes)

    # # # # # # # # 
    # Build and compile model
    # # # # # # # # 
    log("Compiling model...")
    model = ConvNet.build(classes=classes, input_shape=(input_size, 1))

    # # # # # # # # 
    # Train the model
    # # # # # # # # 
    filepath = './results/c' + str(max_class_global) + '-i' + str(inst_global) + '-p' + processing + '/model'
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', save_best_only=True, mode='max')
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, mode='auto', restore_best_weights=True)
    callbacks_list = [checkpoint, early_stopping]

    history = model.fit(X_train, y_train,
                        epochs=40,
                        verbose=VERBOSE,
                        validation_data=(X_valid, y_valid),
                        callbacks=callbacks_list)

    # Save & reload model
    model.save(filepath)
    del model
    model = load_model(filepath)

    # # # # # # # # 
    # Test the model
    # # # # # # # # 
    score = model.evaluate(X_test, y_test,
                           verbose=VERBOSE)
    score_train = model.evaluate(X_train, y_train,
                                 verbose=VERBOSE)

    # # # # # # # # 
    # Print results
    # # # # # # # # 
    log("\n=> Train score:", score_train[0])
    log("=> Train accuracy:", score_train[1])

    log("\n=> Test score:", score[0])
    log("=> Test accuracy:", score[1])

    return score[1], model

        
def GenerateResults(model_file, X_te, y_te):

    model = load_model(model_file)

    probs = model.predict(X_te)
    guesses = [ np.argmax(x) for x in probs ]
    answers = y_te

    num_classes = np.max(answers) + 1

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
        conf_matrix[answers[i], el] += 1

    return conf_matrix


def main():
    """
    """

    # # # # # # # # 
    # Parse arguments
    # # # # # # # # 
    args = parse_arguments()

    global input_length
    global processing

    input_length = args.length
    processing = args.processing

    # # # # # # # # # 
    # # Load the dataset
    # # # # # # # # # 
    print("Loading dataset as type {}...".format(args.attack))

    X, y = load_data(args.traces, typ=args.attack, length=input_size, processing=args.processing)


    global max_class_global
    num_classes = np.max(y) + 1
    max_class_global = num_classes

    global inst_global
    inst_global = math.ceil(X.shape[0] / num_classes)


     
    if not os.path.exists('./results'):
        os.mkdir('./results')

    if not os.path.exists('./results/c' + str(max_class_global) + '-i' + str(inst_global) + '-p' + processing):
        os.mkdir('./results/c' + str(max_class_global) + '-i' + str(inst_global) + '-p' + processing)



    res = []

    folds = args.folds
    count = len(list(y))
    for i in range(folds):
        log("======================")
        log("-- Fold {}".format(i))
        log("======================")
        chunk_start = i*(count//folds)
        chunk_end = (i+1)*(count//folds)
        X_te = X[chunk_start:chunk_end]
        y_te = y[chunk_start:chunk_end]
        if i == 0:
            X_tr = X[chunk_end:, :, :]
            y_tr = y[chunk_end:]
        elif i == folds:
            X_tr = X[:chunk_start, :, :]
            y_tr = y[:chunk_start]
        else:
            X_tr = np.concatenate((X[chunk_end:, :, :], X[:chunk_start, :, :]))
            y_tr = np.concatenate((y[chunk_end:], y[:chunk_start]))
        acc = attack(X_tr, y_tr, X_te[:(count//folds)//2], y_te[:(count//folds)//2], X_te[(count//folds)//2:], y_te[(count//folds)//2:], args, VERBOSE=1)
        res.append(acc)

    log("======================")
    log("-- Summary")
    log("======================")
    log(res)

    global model_file
    model_file = './results/c' + str(max_class_global) + '-i' + str(inst_global) + '-p' + processing + '/model'

    GenerateResults(model_file, X, y)

    # Accuracy, precision, recall, f1, and aoc_roc


if __name__ == "__main__":
    # execute only if run as a script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)


