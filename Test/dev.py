from __future__ import division, print_function
import sys, os
import numpy as np
sys.path.append('/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]))
from GrobnerSolver.polys.multi_cheb import MultiCheb
from GrobnerSolver.polys.multi_power import MultiPower
from GrobnerSolver.grobner.grobner import Grobner
from GrobnerSolver.grobner import maxheap
import pandas as pd
from scipy.linalg import lu





a1 = np.array([[0,1],[-2,0]])
a2 = np.array([[1,0],[0,2]])
c1= MultiPower(a1)
c2 = MultiPower(a2)
grob = Grobner([c1,c2])
grob.add_s_to_matrix()
print(grob.matrix)
raw_input()
grob.add_r_to_matrix()
print(grob.matrix)
raw_input()
print('fs')
print(grob.fs_len)
columns = grob.matrix.columns
print(columns)
P,L,U = lu(grob.matrix.values)
print('U')
print(U)
P_argmax = np.argmax(P,axis=1)
rows_to_keep = P_argmax < grob.fs_len
new_fs = U[rows_to_keep]
new_fs = pd.DataFrame(new_fs,columns=grob.matrix.columns)
new_fs = new_fs[(new_fs.T != 0).any()] # Remove all totally zero rows
new_fs = new_fs.loc[:, (new_fs != 0).any(axis=0)] # Remove all totally zero columns
print(new_fs)
raw_input()
#grob.solve()





#
#a1 = np.arange(2**2).reshape(2,2)
#a2 = np.array([[2,2],[2,2]])
#a3 = np.array([[1,0],[2,0]])
#c1 = MultiCheb(a1)
#c2 = MultiCheb(a2)
#c3 = MultiCheb(a3)
#
#c_list = [c1, c2, c3]
#grob = Grobner(c_list)
#grob.solve()
#






#grob.add_s_to_matrix()
#print(grob.label)
#print('mat')
#print(grob.matrix)
#grob.add_r_to_matrix()
#print(grob.matrix)
#
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

#
#a2 = np.array([[0,0,1],[-2,0,0],[0,0,0]])
#a3 = np.array([[1,0,0],[0,1,0],[-2,0,0]])
#c2 = MultiPower(a2.T)
#c3 = MultiPower(a3.T)
#grob =Grobner([c2,c3])
#grob._build_matrix()
#print(grob.matrix)
#grob.add_s_to_matrix()
#print(grob.matrix)



#print(grob.matrix.columns)
#print(grob.matrix[['[3 1]','[0 1]']])
#self.add_r_to_matrix()
#P,L,U = lu(self.matrix.values)
#P_argmax = np.argmax(P,axis=1)
#rows_to_keep = P_argmax < self.fs_len
#new_fs = U[rows_to_keep]
#new_fs = pd.DataFrame(new_fs,columns=self.matrix.columns)
#new_fs = new_fs[(new_fs.T != 0).any()] # Remove all totally zero rows
#new_fs = new_fs.loc[:, (new_fs != 0).any(axis=0)] # Remove all totally zero columns
##print(new_fs)
##print(list(self.largest_mon.val))
##print(new_fs.index)
#self.polys = self.make_poly_list(new_fs)
#self.f_diff = len(self.polys) - self.f_len
#self.f_len = len(self.polys)
#

#g_basis = grob.solve()
#for g in g_basis:
#    print(g.coeff)




