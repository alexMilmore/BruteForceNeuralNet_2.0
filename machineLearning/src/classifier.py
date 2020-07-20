import pandas as pd
import os
import gc
import numpy as np

import dataHandler as dh
import neuralModel as nModel
import databaseConnect as dbConnect
import translate as tran

# set random seeds
'''
from numpy.random import seed;
seed(1);
from tensorflow import set_random_seed;
set_random_seed(2);
'''

### This program takes data and compares different neural network architectures
#       to see which one is the best

# create database connection
cursor = dbConnect.dbCursor();

# Import tests from the server
testParameters = cursor.readTests();

# create object to handle data importing
importIm = dh.ImageImporter();
importCat = dh.CatagoryImporter();
inputHandler = dh.DataHandler(importIm, importCat);

# Flags for loading new data
currentDataPath = "";
currentDimentions = 0;

for entry in testParameters:
    #try:
    print("Testing");
    fold = 1;
    architecture = tran.textToArchitecture(entry['modelArchitecture']);
    print(architecture);

    # load images from database and generate testing and training data from them
    # imageDimentions sets the resolution of each image
    # inputHandler loads the data in full resolution and then can generate
    # testing and training data at smaller resolutions without reloading data.
    # This is done to prevent having to reload all images when testing different resolutions
    currentData = cursor.lookUpData(entry['dataSet']);
    if ((currentDataPath != currentData['filepath']) or (entry['imageDimentions'] != currentDimentions)):
        catLabels = tran.textToDict(currentData['catagoryDict']);
        inputHandler.read(currentData['filepath'], (entry['imageDimentions'], entry['imageDimentions']), catLabels);
        inputHandler.MLSplit();
        currentDataPath = currentData['filepath'];
        currentDimentions = entry['imageDimentions'];

    # initialise neural net with settings
    inputShape = (entry['imageDimentions'], entry['imageDimentions'], 1);
    classModel = nModel.classifier(architecture, inputHandler);


    classModel.build((None, 64, 64, 1));
    classModel.summary();

    print("train");
    # Train neural net
    classModel.train(entry['epochs'], entry['batchSize']);

    # Upload overview metrics to the database
    # TODO make upload depenent on the number of categories
    print ("Uploading overview to server");
    currentMetrics = classModel.overviewMetrics();
    cursor.inputOverviewToServer(entry['testID'], currentMetrics['loss'], \
    currentMetrics['totalAccuracy'], currentMetrics['classAccuracy']);

    # Upload training metrics to the database
    print ("Uploading training metrics to server");
    trainingMetrics = classModel.getTrainingData();
    for i in range(0, len(trainingMetrics['loss'])):
        # TODO add val_loss
        cursor.inputTrainDataToServer(entry['testID'], fold, i + 1, trainingMetrics['loss'][i]);

    # Upload testing metrics to the database
    print ("Uploading testing metrics to server");
    testMetrics = classModel.getTestingData();
    for i in range(0, len(testMetrics['predictions'])):
        cursor.inputTestDataToServer(entry['testID'], fold, str(testMetrics['predictions'][i]), str(testMetrics['answers'][i]));

    # mark test as completed
    cursor.markCompleted(entry['testID']);

    # Delete model to free memory;
    del classModel;
    gc.collect();
    #except:
    #    cursor.markError(entry['testID']);
    #    print("Error preprocessing this architecture")
