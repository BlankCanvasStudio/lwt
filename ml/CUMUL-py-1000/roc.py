#!/bin/python3

import pandas as pd
import numpy as np
from sklearn.preprocessing import label_binarize
from sklearn.metrics import auc, roc_curve
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

classes_to_display = [ 0, 1 ]

# Load data
file_path = './results/c91-i200-o91-i200/guesses-and-answers.txt'  # replace with your file path
data = pd.read_csv(file_path, header=0, names=['guess', 'answer'])

# Binarize the output
answers = data['answer'].values
guesses = data['guess'].values
classes = sorted(list(set(answers)))  # all unique classes

# Binarize labels
y_test = label_binarize(answers, classes=classes)
y_score = label_binarize(guesses, classes=classes)
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
colors = ['aqua', 'darkorange', 'cornflowerblue']
# for i, color in zip(range(n_classes), colors):
for i in classes_to_display:
    # Find the index of the class to display in the sorted classes list
    class_index = classes.index(i)
    plt.plot(fpr[class_index], tpr[class_index], color=colors[class_index % len(colors)], lw=2,
             label='ROC curve of class {0} (area = {1:0.2f})'
                   ''.format(classes[class_index], roc_auc[class_index]))

plt.plot(fpr["micro"], tpr["micro"], color='deeppink', linestyle=':', linewidth=4,
         label='micro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["micro"]))

plt.plot([0, 1], [0, 1], 'k--', lw=2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Some extension of Receiver operating characteristic to multi-class')
plt.legend(loc="lower right")
plt.show()

