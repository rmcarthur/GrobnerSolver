from __future__ import division, print_function
import sys, os
import numpy as np
sys.path.append('/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]))
from GrobnerSolver.polys.multi_cheb import MultiCheb
from GrobnerSolver.grobner.grobner import Grobner
from GrobnerSolver.grobner import maxheap



#a1 = np.arange(3**3).reshape(3,3,3) 
#a2 = np.arange(3**3).reshape(3,3,3) 
#a1[0,0,0] = 7
#a2[1,1,1] = 9

a1 = np.arange(2**2).reshape(2,2)
a2 = np.array([[2,2],[2,2]])
a3 = np.array([[1,0],[2,0]])
c1 = MultiCheb(a1)
c2 = MultiCheb(a2)
c3 = MultiCheb(a3)
c_list = [c1, c2, c3]
grob = Grobner(c_list)
grob.add_s_to_matrix()
print(grob.polys)
#print(grob.label)
print(grob.matrix)
grob.add_r_to_matrix()

#a3 = np.array([[0,0],[0,1]])
#a4 = np.array([[0,1],[0,0]])
#c3 = MultiCheb(a3)
#c4 = MultiCheb(a4)
#grob2 = Grobner([c3,c4]) 
#s = grob2.calc_s(c3, c4)
#print(s.coeff)
#maxh = maxheap.MaxHeap()
#maxh.heappush((2,1,0,0,0,0))
#maxh.heappush((1,2,2,4,2,4))
#maxh.heappush((2,1,2,4,2,4))
#print(maxh.heappop())
#print(maxh.heappop())



