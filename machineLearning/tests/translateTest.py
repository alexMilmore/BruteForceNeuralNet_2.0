import unittest
import os
import sys
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../src')
sys.path.insert(1, filename)
import translate as tran

class TestTranslateMethods(unittest.TestCase):

    def testTranslateArchitecture(self):
        self.assertEqual(tran.textToArchitecture("dense,32,relu_dense,64,tanh_"), \
        [['dense','32','relu'],['dense','64','tanh']]);
        self.assertEqual(tran.textToArchitecture("conv2D,32,relu_dense,64,tanh_"), \
        [['convFlatten','32','relu'],['dense','64','tanh']]);
        self.assertEqual(tran.textToArchitecture("dense,64,tanh_conv2D,32,relu_"), \
        [['denseTo2D','64','tanh'],['conv2D','32','relu']]);

    def testTranslateDict(self):
        self.assertEqual(tran.textToDict("a=b,c=d,e=f"), {'a':'b', 'c':'d', 'e':'f'});
        self.assertEqual(tran.textToDict("a=0,c=1,e=1"), {'a':0, 'c':1, 'e':1});

if __name__ == '__main__':
    unittest.main()
