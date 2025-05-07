#!/bin/python3

import random
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from torch.utils.data import Dataset, RandomSampler
import torch.optim as optim


# This is to load the csv created by the click recorder
def load_datafile(filename):
    fd = open(filename)
    lines = fd.read()
    data_tuples = lines.split(',')
    arrivals = [ float(x.split(':')[1]) for x in data_tuples ]
    return arrivals


# Create a bunch of splits of the data so it can be passed into NN
# Should this be deterministic?
def split data(data, length):



# Build the conv net for feature embedding
class EmbeddingNet(nn.Module):
    def __init__(self, embedding_size):
        super(EmbeddingNet, self).__init__()
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool1d(kernel_size=3)
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=30, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv1d(30, 20, kernel_size=3)
        self.conv3 = nn.Conv1d(20, embedding_size, kernel_size=3, padding=1)

        # Classification Layers
        self.fc1 = nn.Linear(1385, 693)
        self.fc2 = nn.Linear(693, 5)
        self.softmax = nn.Softmax(dim=1)
    

    def forward(self, x):
        out = self.conv1(x)
        out = self.relu(out)
        out = self.maxpool(out)
        out = self.conv2(out)
        out = self.relu(out)
        out = self.maxpool(out)
        out = self.conv3(out)

        # Convert to flatness
        out = out.view(-1, 1385)

        out = self.fc1(out)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out
    
    def embed(self, data):
        out = self.conv1(x)
        out = self.relu(out)
        out = self.maxpool(out)
        out = self.conv2(out)
        out = self.relu(out)
        out = self.maxpool(out)
        out = self.conv3(out)
        return out


class CustomDataset(Dataset):
    def __init__(self, data, label):
        self.data = data
        self.label = label

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        sample = torch.from_numpy(self.data[index]).unsqueeze(0).float()
        return sample, self.label[index]


def label_to_one_hot(label, options):
    data = np.zeros(options)
    data[label] = 1
    return data




t_labels = np.array(labels)
np_data_ordered = np.array(data)

# Shuffle the datasets
permutation = np.random.permutation(len(np_data_ordered))
t_labels = t_labels[permutation]
np_data_all = np_data_ordered[permutation]


# Now that we have numpy data, lets build a training set
training_data = np_data_all[:300]
training_labels = t_labels[:300]

testing_data = np_data_all[300:400]
testing_labels = t_labels[300:400]

np_validation = np_data_all[400:]


t_data = torch.from_numpy(training_data).unsqueeze(1).float()

torch_data = CustomDataset(training_data, training_labels)
testing_data = CustomDataset(testing_data, testing_labels)

# Create a custom data loader
batch_size = 1
dataloader = torch.utils.data.DataLoader(torch_data, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(testing_data)

num_classes = 5
model = EmbeddingNet(num_classes)


crit = nn.CrossEntropyLoss()
opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)



num_epochs = 10

for epoch in range(num_epochs):
    running_loss = 0.0
    start_time = datetime.now()

    for i, tup in enumerate(dataloader, 0):
        batch_data, label = tup
        encoded_label = label_to_one_hot(label, num_classes)

        opt.zero_grad()

        outputs = model(batch_data)
        loss = crit(outputs, label)
        loss.backward()

        opt.step()

        running_loss += loss.item()
        if i % 500 == 499:
            print(f'Epoch: {epoch + 1}, Batch: {i + 1}, Loss: {running_loss / 1000}')
            running_loss = 0.0

    end_time = datetime.now()
    print('Time for epoch: ', end_time - start_time)
        


# Lets eval the model

model.eval()

# Initialize variables for tracking accuracy
total_samples = 0
correct_predictions = 0

# Disable gradient computation
with torch.no_grad():
    for images, labels in test_loader:
        # Forward pass through the network
        outputs = model(images)
        
        # Get the predicted labels
        _, predicted = torch.max(outputs.data, 1)
        
        # Count the number of correct predictions
        correct_predictions += (predicted == labels).sum().item()
        
        # Increment the total number of samples
        total_samples += labels.size(0)

# Calculate the accuracy
accuracy = correct_predictions / total_samples
print(f"Accuracy: {accuracy * 100}%")

