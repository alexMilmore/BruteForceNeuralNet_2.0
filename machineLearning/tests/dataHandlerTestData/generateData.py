import numpy as np
from PIL import Image
import os

# All pixels in these images perfectly divide by 3, this tests the basic averaging
# 3 images
def generateIntTestBW(path, filetype):

    try:
        os.mkdir(path + '/dataHandlerTestData/averageTestData');
    except:
        print("Didn't make new dir, filepath exists")

    ar1 = np.array([[10,40,30,50],[20,40,50,30],[90,30,20,60],[20,30,40,20]], dtype=np.uint8);
    ar2 = np.array([[40,40,30,10],[30,20,50,30],[30,20,50,40],[10,60,20,50]], dtype=np.uint8);
    ar3 = np.array([[10,40,60,30],[40,30,20,30],[30,40,50,20],[60,30,30,20]], dtype=np.uint8);

    img1 = Image.fromarray(ar1, "L");
    img2 = Image.fromarray(ar2, "L");
    img3 = Image.fromarray(ar3, "L");

    img1.save(path + '/dataHandlerTestData/averageTestData/im1.' + filetype);
    img2.save(path + '/dataHandlerTestData/averageTestData/im2.' + filetype);
    img3.save(path + '/dataHandlerTestData/averageTestData/im3.' + filetype);

    avgIm = np.array([[20,40,40,30],[30,30,40,30],[50,30,40,40],[30,40,30,30]]);

    return avgIm;

def generateIntTestRGB(filetype):
    print("under construction")

# These ones do not divide by 3, this tests average images when integer division
# gets in the way


## Who unit tests the unit tester??
if __name__=="__main__":
    generateIntTest('.png');
