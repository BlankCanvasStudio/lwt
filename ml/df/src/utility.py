# import cPickle as pickle
import numpy as np
import os, traceback, struct, sys

# Read the binary format and return an array of the timing array and sizing array
def read_data(path, length=5000):
    fd = open(path, 'rb')
    # size, time
    [ sizes, times, direction ] = [ np.zeros(length, dtype=int), np.zeros(length, dtype=np.float64), np.zeros(length, dtype=int) ]

    fd.seek(4)
    offset = struct.unpack('d', fd.read(8))[0]
    file_size = os.path.getsize(path)

    index = 0

    while fd.tell() < file_size and index < length:
        size = int.from_bytes(fd.read(4), sys.byteorder)
        time = struct.unpack('d', fd.read(8))[0]
        sizes[index] = size
        times[index] = time - offset
        index += 1

    fd.close()

    # Remove all values outside the int range
    mask = (times < -sys.maxsize - 1) | (times > sys.maxsize)
    # Convert values outside the range to zero
    times[mask] = 0


    return [ sizes, times, direction ]


def format_data(sizes, times):
    return times


# This reads a file and returns an array of arrays:
    # [ [timestamp],  [direction] ]
    # timstamp is a float
    # direction is either +1 or -1
def load_trace(path, seperator="\t", length=5000):
    """
    loads data to be used for predictions
    """

    [ sizes, times, direction ] = read_data(os.path.join(path, "pipe_rcv.csv"), length=length)

    # Cleans up data and does inference
    times = format_data(sizes, times)

    # Return the sequence data but no directionality can be found
    return [ sizes, times, direction ]

# Load data for non-defended dataset for CW setting
def LoadDataNoDefCW(typ = 2, length=5000):

    print("Loading non-defended dataset for closed-world scenario")
    # Point to the directory storing data
    directory = '../../tiktok/cw-ow-timing-class/data'

    X, y = [], []
    class_counter = 0
    for dir in os.listdir(directory):
        try:
            cls, inst  = dir.split('-')
            trace_class = int(cls)
            # build direction sequence
            [ size, times, direction ] = load_trace(os.path.join(directory, dir), length=length)
            # print(sequence)

            # This actually builds out the array
            # use time direction
            if typ==1:
                sequence = np.multiply(times, direction)
            # use time only
            elif typ==2:
                sequence = times.copy()
            # use direction only
            else:
                sequence = direction.copy()

            del size
            del times
            del direction

            sequence.resize((length, 1))
            X.append(sequence)
            y.append(trace_class)

        except Exception as e:
            print("Error for", dir)
            print(e)
            traceback.print_exc()
            print('\n\n')
            pass

    # wrap as numpy array
    X, Y = np.array(X), np.array(y)

    # print(X)
    # print(Y)

    # shuffle
    s = np.arange(Y.shape[0])
    np.random.seed(0)
    np.random.shuffle(s)
    X, Y = X[s], Y[s]

    # print(X)
    # print(Y)

    total_length = len(Y)
    test_length = int(0.1 * total_length)
    train_length = int(0.8 * total_length)

    return X[:train_length], Y[:train_length], X[train_length:train_length + test_length], Y[train_length:train_length + test_length], X[train_length + test_length:], Y[train_length + test_length:]



"""

    print("Loading non-defended dataset for closed-world scenario")
    # Point to the directory storing data
    dataset_dir = '../dta'

    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open(dataset_dir + 'X_train_NoDef.pkl', 'rb') as handle:
        X_train = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_train_NoDef.pkl', 'rb') as handle:
        y_train = np.array(pickle.load(handle))

    # Load validation data
    with open(dataset_dir + 'X_valid_NoDef.pkl', 'rb') as handle:
        X_valid = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_valid_NoDef.pkl', 'rb') as handle:
        y_valid = np.array(pickle.load(handle))

    # Load testing data
    with open(dataset_dir + 'X_test_NoDef.pkl', 'rb') as handle:
        X_test = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_test_NoDef.pkl', 'rb') as handle:
        y_test = np.array(pickle.load(handle))

    print("Data dimensions:")
    print("X: Training data's shape : ", X_train.shape)
    print("y: Training data's shape : ", y_train.shape)
    print("X: Validation data's shape : ", X_valid.shape)
    print("y: Validation data's shape : ", y_valid.shape)
    print("X: Testing data's shape : ", X_test.shape)
    print("y: Testing data's shape : ", y_test.shape)

    return X_train, y_train, X_valid, y_valid, X_test, y_test

# Load data for non-defended dataset for CW setting
def LoadDataWTFPADCW():

    print( "Loading WTF-PAD dataset for closed-world scenario")
    # Point to the directory storing data
    dataset_dir = '../dataset/ClosedWorld/WTFPAD/'

    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open(dataset_dir + 'X_train_WTFPAD.pkl', 'rb') as handle:
        X_train = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_train_WTFPAD.pkl', 'rb') as handle:
        y_train = np.array(pickle.load(handle))

    # Load validation data
    with open(dataset_dir + 'X_valid_WTFPAD.pkl', 'rb') as handle:
        X_valid = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_valid_WTFPAD.pkl', 'rb') as handle:
        y_valid = np.array(pickle.load(handle))

    # Load testing data
    with open(dataset_dir + 'X_test_WTFPAD.pkl', 'rb') as handle:
        X_test = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_test_WTFPAD.pkl', 'rb') as handle:
        y_test = np.array(pickle.load(handle))

    print("Data dimensions:")
    print("X: Training data's shape : ", X_train.shape)
    print("y: Training data's shape : ", y_train.shape)
    print("X: Validation data's shape : ", X_valid.shape)
    print("y: Validation data's shape : ", y_valid.shape)
    print("X: Testing data's shape : ", X_test.shape)
    print("y: Testing data's shape : ", y_test.shape)

    return X_train, y_train, X_valid, y_valid, X_test, y_test

# Load data for non-defended dataset for CW setting
def LoadDataWalkieTalkieCW():

    print("Loading Walkie-Talkie dataset for closed-world scenario")
    # Point to the directory storing data
    dataset_dir = '../dataset/ClosedWorld/WalkieTalkie/'

    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open(dataset_dir + 'X_train_WalkieTalkie.pkl', 'rb') as handle:
        X_train = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_train_WalkieTalkie.pkl', 'rb') as handle:
        y_train = np.array(pickle.load(handle))

    # Load validation data
    with open(dataset_dir + 'X_valid_WalkieTalkie.pkl', 'rb') as handle:
        X_valid = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_valid_WalkieTalkie.pkl', 'rb') as handle:
        y_valid = np.array(pickle.load(handle))

    # Load testing data
    with open(dataset_dir + 'X_test_WalkieTalkie.pkl', 'rb') as handle:
        X_test = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_test_WalkieTalkie.pkl', 'rb') as handle:
        y_test = np.array(pickle.load(handle))

    print("Data dimensions:")
    print("X: Training data's shape : ", X_train.shape)
    print("y: Training data's shape : ", y_train.shape)
    print("X: Validation data's shape : ", X_valid.shape)
    print("y: Validation data's shape : ", y_valid.shape)
    print("X: Testing data's shape : ", X_test.shape)
    print("y: Testing data's shape : ", y_test.shape)

    return X_train, y_train, X_valid, y_valid, X_test, y_test

# Load data for non-defended dataset for OW training
def LoadDataNoDefOW_Training():

    print("Loading non-defended dataset for open-world scenario for training")
    # Point to the directory storing data
    dataset_dir = '../dataset/OpenWorld/NoDef/'

    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open(dataset_dir + 'X_train_NoDef.pkl', 'rb') as handle:
        X_train = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_train_NoDef.pkl', 'rb') as handle:
        y_train = np.array(pickle.load(handle))

    # Load validation data
    with open(dataset_dir + 'X_valid_NoDef.pkl', 'rb') as handle:
        X_valid = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_valid_NoDef.pkl', 'rb') as handle:
        y_valid = np.array(pickle.load(handle))


    print("Data dimensions:")
    print("X: Training data's shape : ", X_train.shape)
    print("y: Training data's shape : ", y_train.shape)
    print("X: Validation data's shape : ", X_valid.shape)
    print("y: Validation data's shape : ", y_valid.shape)

    return X_train, y_train, X_valid, y_valid

# Load data for non-defended dataset for OW evaluation
def LoadDataNoDefOW_Evaluation():

    print("Loading non-defended dataset for open-world scenario for evaluation")
    # Point to the directory storing data
    dataset_dir = '../dataset/OpenWorld/NoDef/'

    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open(dataset_dir + 'X_test_Mon_NoDef.pkl', 'rb') as handle:
        X_test_Mon = pickle.load(handle)
    with open(dataset_dir + 'y_test_Mon_NoDef.pkl', 'rb') as handle:
        y_test_Mon = pickle.load(handle)
    with open(dataset_dir + 'X_test_Unmon_NoDef.pkl', 'rb') as handle:
        X_test_Unmon = pickle.load(handle)
    with open(dataset_dir + 'y_test_Unmon_NoDef.pkl', 'rb') as handle:
        y_test_Unmon = pickle.load(handle)

    X_test_Mon = np.array(X_test_Mon)
    y_test_Mon = np.array(y_test_Mon)
    X_test_Unmon = np.array(X_test_Unmon)
    y_test_Unmon = np.array(y_test_Unmon)

    return X_test_Mon, y_test_Mon, X_test_Unmon, y_test_Unmon

# Load data for WTF-PAD dataset for OW training
def LoadDataWTFPADOW_Training():

    print("Loading WTF-PAD dataset for open-world scenario for training")
    # Point to the directory storing data
    dataset_dir = '../dataset/OpenWorld/WTFPAD/'

    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open(dataset_dir + 'X_train_WTFPAD.pkl', 'rb') as handle:
        X_train = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_train_WTFPAD.pkl', 'rb') as handle:
        y_train = np.array(pickle.load(handle))

    # Load validation data
    with open(dataset_dir + 'X_valid_WTFPAD.pkl', 'rb') as handle:
        X_valid = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_valid_WTFPAD.pkl', 'rb') as handle:
        y_valid = np.array(pickle.load(handle))


    print("Data dimensions:")
    print("X: Training data's shape : ", X_train.shape)
    print("y: Training data's shape : ", y_train.shape)
    print("X: Validation data's shape : ", X_valid.shape)
    print("y: Validation data's shape : ", y_valid.shape)

    return X_train, y_train, X_valid, y_valid

# Load data for WTF-PAD dataset for OW evaluation
def LoadDataWTFPADOW_Evaluation():

    print("Loading WTF-PAD dataset for open-world scenario for evaluation")
    # Point to the directory storing data
    dataset_dir = '../dataset/OpenWorld/WTFPAD/'

    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open(dataset_dir + 'X_test_Mon_WTFPAD.pkl', 'rb') as handle:
        X_test_Mon = pickle.load(handle)
    with open(dataset_dir + 'y_test_Mon_WTFPAD.pkl', 'rb') as handle:
        y_test_Mon = pickle.load(handle)
    with open(dataset_dir + 'X_test_Unmon_WTFPAD.pkl', 'rb') as handle:
        X_test_Unmon = pickle.load(handle)
    with open(dataset_dir + 'y_test_Unmon_WTFPAD.pkl', 'rb') as handle:
        y_test_Unmon = pickle.load(handle)

    X_test_Mon = np.array(X_test_Mon)
    y_test_Mon = np.array(y_test_Mon)
    X_test_Unmon = np.array(X_test_Unmon)
    y_test_Unmon = np.array(y_test_Unmon)

    return X_test_Mon, y_test_Mon, X_test_Unmon, y_test_Unmon

# Load data for WalkieTalkie dataset for OW training
def LoadDataWalkieTalkieOW_Training():

    print("Loading Walkie-Talkie dataset for open-world scenario for training")
    # Point to the directory storing data
    dataset_dir = '../dataset/OpenWorld/WalkieTalkie/'

    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open(dataset_dir + 'X_train_WalkieTalkie.pkl', 'rb') as handle:
        X_train = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_train_WalkieTalkie.pkl', 'rb') as handle:
        y_train = np.array(pickle.load(handle))

    # Load validation data
    with open(dataset_dir + 'X_valid_WalkieTalkie.pkl', 'rb') as handle:
        X_valid = np.array(pickle.load(handle))
    with open(dataset_dir + 'y_valid_WalkieTalkie.pkl', 'rb') as handle:
        y_valid = np.array(pickle.load(handle))


    print("Data dimensions:")
    print("X: Training data's shape : ", X_train.shape)
    print("y: Training data's shape : ", y_train.shape)
    print("X: Validation data's shape : ", X_valid.shape)
    print("y: Validation data's shape : ", y_valid.shape)

    return X_train, y_train, X_valid, y_valid

# Load data for WTF-PAD dataset for OW evaluation
def LoadDataWalkieTalkieOW_Evaluation():

    print("Loading Walkie-Talkie dataset for open-world scenario for evaluation")
    # Point to the directory storing data
    dataset_dir = '../dataset/OpenWorld/WalkieTalkie/'

    # X represents a sequence of traffic directions
    # y represents a sequence of corresponding label (website's label)

    # Load training data
    with open(dataset_dir + 'X_test_Mon_WalkieTalkie.pkl', 'rb') as handle:
        X_test_Mon = pickle.load(handle)
    with open(dataset_dir + 'y_test_Mon_WalkieTalkie.pkl', 'rb') as handle:
        y_test_Mon = pickle.load(handle)
    with open(dataset_dir + 'X_test_Unmon_WalkieTalkie.pkl', 'rb') as handle:
        X_test_Unmon = pickle.load(handle)
    with open(dataset_dir + 'y_test_Unmon_WalkieTalkie.pkl', 'rb') as handle:
        y_test_Unmon = pickle.load(handle)

    X_test_Mon = np.array(X_test_Mon)
    y_test_Mon = np.array(y_test_Mon)
    X_test_Unmon = np.array(X_test_Unmon)
    y_test_Unmon = np.array(y_test_Unmon)

    return X_test_Mon, y_test_Mon, X_test_Unmon, y_test_Unmon
"""
