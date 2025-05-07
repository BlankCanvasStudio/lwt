#!/bin/python3

import pandas as pd
import numpy as np
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from itertools import cycle

# classes_to_display = [ 45, 34, 21, 9, 0 ] #range(0, 55)
# classes_to_display = range(0, 91)
classes_to_display = []


# Load data
file_path = './results/c91-i200-o91-i200/guesses-and-answers.txt'
loaded_data = np.loadtxt(file_path, delimiter=',', skiprows=1)
answers = loaded_data[:, 0].astype(int)
y_score = loaded_data[:, 1:]

# Ensure y_score is a probability distribution
if y_score.max() > 1 or y_score.min() < 0:
    raise ValueError("y_score values should be probabilities between 0 and 1")

# Get unique classes
classes = sorted(list(set(answers)))

# Binarize labels
y_test = label_binarize(answers, classes=classes)
n_classes = y_test.shape[1]

# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and ROC area
fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

# Plot all ROC curves
plt.figure()
colors = cycle([
    'aqua', 'darkorange', 'cornflowerblue',
    'green', 'red', 'purple', 'yellow', 'brown', 'pink', 'grey', 'olive', 'cyan',
    'magenta', 'navy', 'teal', 'lime', 'indigo', 'gold', 'crimson', 'lavender',
    'maroon', 'turquoise', 'beige', 'coral', 'plum', 'khaki', 'orchid',
    'salmon', 'sienna', 'silver', 'tan', 'thistle', 'violet', 'wheat'
])
for i in classes_to_display:
    plt.plot(fpr[i], tpr[i], color=next(colors), lw=2,
             label='ROC curve of class {0} (area = {1:0.2f})'
                   ''.format(classes[i], roc_auc[i]))

plt.plot(fpr["micro"], tpr["micro"], color='deeppink', linestyle=':', linewidth=4,
         label='micro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["micro"]))

plt.plot([0, 1], [0, 1], 'k--', lw=2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic for kFP')
plt.legend(loc="lower right")
plt.show()

