import numpy as np
import os, sys
sys.path.append('/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]))
from GrobnerSolver.polys.multi_power import MultiPower
from GrobnerSolver.grobner.grobner import Grobner
import unittest

class TestGrobner(unittest.TestCase):

    def test_s_poly(self):
        a2 = np.array([[0,0,0,1],[0,-2,0,0],[0,0,0,0],[0,0,0,0]])
        a3 = np.array([[0,1,0,0],[0,0,1,0],[-2,0,0,0],[0,0,0,0]])
        c2 = MultiPower(a2.T)
        c3 = MultiPower(a3.T)
        grob = Grobner([c2,c3])
        s1 = np.round(grob.calc_s(c2,c3).coeff)
        true_s = np.array([[0,0,0,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.assertTrue(s1.all() == true_s.all())


if __name__ == '__main__':
    unittest.main()




