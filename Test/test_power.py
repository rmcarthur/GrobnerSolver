import numpy as np
import os,sys
sys.path.append('/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-2]))
from cheb.polys.multi_power import MultiPower
import unittest

class TestMultiCheb(unittest.TestCase):

    def test_add(self):
        a1 = np.arange(27).reshape((3,3,3))
        Test2 = MultiPower(a1)
        a2 = np.ones((3,3,3))
        Test3 = MultiPower(a2)
        addTest = Test2 + Test3
        self.assertTrue(addTest.coeff.all() == (Test2.coeff + Test3.coeff).all())

    def test_mult(self):
        test1 = np.array([[0,1],[2,1]])
        test2 = np.array([[2,2],[3,0]])
        p1 = MultiPower(test1)
        p2 = MultiPower(test2)
        new_poly = p1*p2
        truth = np.array([[0, 2, 2],[4,9,2],[6,3,0]])
        test = np.allclose(new_poly.coeff, truth)
        self.assertTrue(test)
        


if __name__ == '__main__':
    unittest.main()




