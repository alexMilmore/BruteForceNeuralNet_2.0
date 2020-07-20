import numpy as np
import os
from tqdm import tqdm
import cv2
import random
from sklearn.utils import shuffle
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import pandas as pd

class DataHandler:
    def __init__(self, inputImporter, targetImporter):
        self.inputImporter = inputImporter;
        self.targetImporter = targetImporter;
        self.input = inputImporter.data;
        self.target = targetImporter.data;

    def read(self, filepath, inputSetting, targetSetting):
        self.inputImporter.read(filepath, inputSetting);
        self.targetImporter.read(filepath, targetSetting);
        self.input = self.inputImporter.data;
        self.target = self.targetImporter.data;

    def shuffle(self):
        self.input, self.target = shuffle(self.input, self.target);

    def MLSplit(self):
        # Split data into training, testing and validation data
        self.x_train, self.x_val, self.y_train, self.y_val = train_test_split(self.input, self.target, random_state = 0);
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x_train, self.y_train, random_state = 0);
        self.calcWeights();

    # If the target is a set of  catagories, we want to be able to weight
    # the answers based on the number of each catagory
    def calcWeights(self):
        if (self.targetImporter.name == 'Cat'):
            self.trainWeights, self.trainCatCounts = self.__calculateWeights(self.y_train);
            self.valWeights,  self.valCatCounts= self.__calculateWeights(self.y_val);
            self.testWeights, self.testCatCounts = self.__calculateWeights(self.y_test);

    # calculates weights of dataset before it has been hot encoded
    # takes in hot encoded list of catagories, calculates the number and ratio
    # of each
    def __calculateWeights(self, data):
        weights = {};
        catagoryCounts = np.zeros(data.shape[1]);

        # Counts number of each catagory
        for i in range(data.shape[0]):
            catagoryCounts = np.add(catagoryCounts, data[i]);

        for i in range(0, len(catagoryCounts)):
            weights[i] = float(catagoryCounts[i]/data.shape[0]);

        return weights, catagoryCounts

# Each importer creates an array of the object the importer is defined for labelled
# using the file name, a dataHandler is used to relate these arrays and generate
# ML data
class ImageImporter:
    def __init__(self):
        self.name = 'Img';
        self.average = None;
        self.minVal = 0;
        # raw data is stored in uint8 so it is smaller
        self.rawData = None;
        # data is stored as a float, but is usually a smaller resolution than
        # raw data to prevent killing the computer
        self.data = None;

    # Images may be a different resolutions, filetypes and colour encodings
    def readRaw(self, filepath):
        data = [];
        for imageFileName in tqdm(os.listdir(filepath)):
            im = self.__imread(imageFileName, filepath)
            data.append(im);

        self.rawData = np.asarray(data);

    # takes the raw data and generates a consistant set of images
    def read(self, filepath, shape):
        self.readRaw(filepath);
        datashape = (self.rawData.shape[0], shape[0], shape[1]);
        data = np.zeros(datashape, dtype=np.float);

        for i in range (0, self.rawData.shape[0]):
            data[i] = cv2.resize(self.rawData[i], shape);

        # removing the average from the images aids machine learning
        self.average = self.__findAverageImg(data);
        data = self.__removeAverageImg(data);

        # Data is normalzed between 0-1, this helps certain neural net activation
        # functions such as sigmoid that saturate over 1
        for i in range (0, self.rawData.shape[0]):
            im = np.array(data[i], dtype=np.float);
            data[i] = im/255;

        data = data[..., np.newaxis]; # add dimention so keras can read

        self.data = data;

    # reads an image
    def __imread(self, image, imagePath):
        path = os.path.join(imagePath,image)  # create path image
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE);
        return image;

    ################################ Data cleaning ############################
    # Calculate the average image in the dataset
    def __findAverageImg(self, data):
        # using uint32 over 16 million images can be averaged over without a
        # chance of overflow. This should be fine
        sumImg = np.zeros(data[0].shape, dtype = np.uint32);
        numOfImages = data.shape[0];
        for i in range(0, numOfImages):
            sumImg = np.add(sumImg, data[i]);

        sumImg = sumImg/numOfImages
        sumImg = np.array(sumImg, dtype = np.double)
        return sumImg;

    # removing the average helps machine learning by preventing the model from
    # simply learning the average
    def __removeAverageImg(self, data):
        # find minimum value of image - average. This must be accounted for to
        # prevent underflow
        mem = np.zeros(data.shape[0]);
        for i in range(0, data.shape[0]):
            # int16 is the smallest numpy datatype that will fit all numbers
            # in uint8 and allows negative numbers
            check = np.array(data[i], dtype=np.int16) - np.array(self.average, dtype=np.int16);
            mem[i] = check.min();

        self.minVal = mem.min();

        # remove average image and fix underlow errors
        for i in range(0, data.shape[0]):
            data[i] = data[i] - self.average + self.minVal;

        return data

    # normalizing the dataset helps machine learning as many activation Functions
    # (sigmoid, tanh) saturate above 1
    def __normalizeImage(self, data):
        # scale so all pixel values are between 0-1
        data = np.array(data, dtype=np.float);
        for i in range(0, data.shape[0]):
            data[i] = data[i]/self.maxVal;
        return data;

    def reconstructImg(self, img):
        reconImg = img * self.maxVal + self.minVal;
        reconImg = np.add(reconImg, self.average);
        reconImg = np.array(reconImg, dtype=np.uint8)
        return reconImg[:,:,0];

class CatagoryImporter:
    def __init__(self):
        self.name = 'Cat';
        self.data = None;

    def read(self, filepath, catagoryLabels):
        data = [];
        keys = catagoryLabels.keys();

        for fileName in os.listdir(filepath):
            for key in keys:
                if (fileName.find(key) != -1):
                    data.append([catagoryLabels[key]]);

        data = np.asarray(data);
        self.data = self.__encodeData(data);

    # data must be encoded for use with keras
    def __encodeData(self, classifications):
        encoder = OneHotEncoder(sparse = False);
        classifications = encoder.fit_transform(classifications);
        return classifications

# TODO .csv importer
#class CsvImporter:

if __name__=="__main__":
    images = ImageImporter();

    catagories = CatagoryImporter();

    handler = DataHandler(images,catagories);
    handler.read("/home/alex/Documents/mipDataCollections/mipDataBest", \
    (128, 128), \
    {"HV":0, "PA":1, "PT":1});
    #handler.MLSplit();
