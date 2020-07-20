import unittest
import os
import sys
import numpy as np
import cv2

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../src')
sys.path.insert(1, filename)
import dataHandler as dh

filename = os.path.join(dirname, 'dataHandlerTestData')
sys.path.insert(1, filename)
import generateData


class TestImageImporterMethods(unittest.TestCase):
    def testAverageImg(self):
        # generate testing images
        avgImg = generateData.generateIntTestBW(dirname, 'png');
        # read in images
        images = dh.ImageImporter(256);
        images.read("dataHandlerTestData/averageTestData", 0);
        # this test is only a true false, so it's good to have a look at the
        # difference if something goes wrong
        print ("Should be:")
        print(avgImg);
        print("Calculated:")
        print(images.average);
        self.assertTrue(np.all(images.average == avgImg));

    def testNormalisation(self):
        path = "dataHandlerTestData/data1";
        images = dh.ImageImporter(256);
        images.read(path, 0);
        self.assertLessEqual(images.data.max(), 1);
        self.assertGreater(images.data.max(), 0);

'''
    # TODO reconstruction dosen't work
    def testReconstruct(self):
        path = "dataHandlerTestData/data1";
        # import normalized images
        images = dh.ImageImporter(256);
        images.read(path, 0);

        # import unnormalized images
        imList = []
        for imageFileName in os.listdir(path):
            path = os.path.join(path,imageFileName);  # create path image
            imList.append(cv2.imread(path, cv2.IMREAD_GRAYSCALE));
        imList = np.array(imList);

        for i in range(0, len(imList)):
            # check if reconstructions are the same as unnormalized images
            self.assertEqual(images.reconstructImg(images.data[i]).shape, imList[i].shape);
            # this test is only a true false, so it's good to have a look at the
            # difference if something goes wrong
            print ("Should be:");
            print(imList[i]);
            print("Calculated:");
            print(images.reconstructImg(images.data[i]));
            self.assertTrue(np.all(images.reconstructImg(images.data[i]) == imList[i]));
'''

class TestCatagoryImporterMethods(unittest.TestCase):
    def testRead(self):
        catagories = dh.CatagoryImporter();
        catagories.read("dataHandlerTestData/data1", {'HV':0, 'PV':1});
        self.assertEqual(catagories.data.shape, (8,2));
        self.assertEqual(np.sum(catagories.data[:,0]), 5);
        self.assertEqual(np.sum(catagories.data[:,1]), 3);

class TestDataHandlerMethods(unittest.TestCase):
    def testMLSplit(self):
        images = dh.ImageImporter(256);
        catagories = dh.CatagoryImporter();
        dataHandler = dh.DataHandler(images, catagories);
        dataHandler.read("dataHandlerTestData/data1", {"HV":0, "PV":1});
        dataHandler.MLSplit();

        # As this is a random split, a good unit test can't be built. This one
        # has to be done my eye
        # TODO improve these tests
        print(dataHandler.trainWeights);
        print(dataHandler.valWeights);
        print(dataHandler.testWeights);
        print(dataHandler.trainCatCounts);
        print(dataHandler.valCatCounts);
        print(dataHandler.testCatCounts);

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
