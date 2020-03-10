#test function =
#arrays of different lengths
#multiple columned array for y
#non-arrays so strings, integers falan

import unittest
from linreg import *
import csv

class linregTest(unittest.TestCase):

    def test_interror(self):
        with self.assertRaises(AttributeError):
            linreg(1, 2)

    def test_lengtherror(self):
        expv = np.random.randint(10, size=(10, 3))
        depv = np.random.randint(10, size=(15, 1))
        with self.assertRaises(ValueError):
            linreg(depv, expv)

    def test_ylengtherror(self):
        depv = np.random.randint(10, size=(10,3))
        expv = np.random.randint(10, size=(10,2))
        with self.assertRaises(ValueError):
            linreg(depv, expv)

    def test_stringinarray(self):
        depv = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,'string'])
        expv = np.random.randint(15, size=(15, 2))
        with self.assertRaises(UFuncTypeError):
            linreg(depv, expv)
            
if __name__ == '__main__':
    unittest.main()
