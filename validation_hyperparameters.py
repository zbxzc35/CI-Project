import NeuralNetwork
import pickle
#from random import shuffle
import random
import numpy as np
import externalFunctions


with open('./data_dump/objs.pickle_train') as f:
    dataset_data, dataset_labels = pickle.load(f)


with open('./data_dump/objs.pickle_test') as f:
    validation_data, validation_labels = pickle.load(f)

# Shuffle the dataset
# data_shuf = []
# labels_shuf = []
# index_shuf = range(len(dataset_labels))
# random.shuffle(index_shuf)
# for i in index_shuf:
#     data_shuf.append(dataset_data[i])
#     labels_shuf.append(dataset_labels[i])


# We will train over a smaller train dataset for finding hyperparameters
train_data = dataset_data[0:10000]
train_labels = dataset_labels[0:10000]
validation_data = dataset_data[10000:11000]
validation_labels = validation_labels[10000:11000]


learning_rates = np.logspace(-3,0,15)
#regularization_terms = np.logspace(-3, 0, 10)
number_epochs = range(2,70)
number_hidden_units = range(50,151)

number_trials = [10,20,50,100]

best_validation_precision = []
best_hyp_parameters_list = []


for trials in number_trials:
    validation_metrics = []
    hyp_parameters_list = []
    for i in range(trials):
        learning_rate = random.choice(learning_rates)
        #regularization_term = random.choice(regularization_terms)
        number_epoch = random.choice(number_epochs)
        hidden_units = random.choice(number_hidden_units)

        # Set of hyperparameters
        hyp_parameters = [learning_rate, 0,
                          number_epoch, hidden_units]


        print 'Values of hyperparameters:'
        print 'learning rate: {}'.format(learning_rate)
        print 'regularization term: {}'.format(0)
        print 'number of epochs: {}'.format(number_epoch)
        print 'hidden units: {}'.format(hidden_units)

        # Train
        nn = NeuralNetwork.NeuralNetwork(150, hidden_units, 1)
        nn.SGDbackProp(dataset_data, dataset_labels,number_epoch,
                        learning_rate,0)
        #nn.SGDbackProp(train_data, train_labels,10,
        #               0.01,0.001)
                       #validation_data=validation_data,
                       #validation_labels=validation_labels)


        validation_metrics.append(externalFunctions.getPrecisionRecallSupport(nn, validation_data, validation_labels)[0][1])
        hyp_parameters_list.append(hyp_parameters)
        print '{} Validation precision for person: {}'.format(trials,validation_metrics[-1])

    best_validation_precision.append(max(validation_metrics))
    best_hyp_parameters_list.append(hyp_parameters_list[validation_metrics.index(max(validation_metrics))])




