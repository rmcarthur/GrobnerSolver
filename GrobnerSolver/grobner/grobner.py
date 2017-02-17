from __future__ import print_function, division
import fractions
import itertools
import numpy as np
import pandas as pd
import maxheap
import os,sys
sys.path.append('/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-2]))
from GrobnerSolver.polys.multi_cheb import MultiCheb
from GrobnerSolver.polys.multi_power import MultiPower
from scipy.linalg import lu

class Grobner(object):

    def __init__(self,polys):
        '''
        polys -- a list of polynomials that generate your ideal
        self.org_len - Orginal length of the polys passed in
        '''
        self.polys = polys
        self.f_len = len(polys)
        self.largest_mon = maxheap.TermOrder(tuple((0,0,0,0)))
        self.matrix = pd.DataFrame()
        self.label = []
        self.label_count = 0
        self.np_matrix = np.zeros([0,0])
        self.term_set = set()
        self.term_dict = {}
        self._build_matrix()

    def solve(self):
        for i in xrange():
            self.add_s_to_matrix()
            self.add_r_to_matrix()
            P,L,U = lu(self.matrix.values)
            P_argmax = np.argmax(P,axis=1)
            rows_to_keep = P_argmax < self.fs_len
            new_fs = U[rows_to_keep]
            print('new_fs')
            print(self.matrix.columns)
            print(new_fs)


    def _build_matrix(self):
        """
        #TODO: Fix this to just use numpy arrays. You can sort, using numpy arg sort
    
        returns:
        matrix - Pandas DataFrame object with the polynomials indexed
        """
        for poly in self.polys:
            #For each polynomial, make a matrix object, and add its column
            submatrix = pd.DataFrame()
            sub_np = []
            for idx in poly.grevlex_gen():
                idx_term = maxheap.TermOrder(tuple(idx)) # Used to get an ordering on terms
                if not idx_term.val in self.term_set:
                    self.term_set.add(idx_term.val)
                    self.label.append(tuple(idx)) # Put the actual tuple of index into a list
                submatrix[str(idx)] = pd.Series([poly.coeff[tuple(idx)]])
            #Append all submatracies
            self.matrix = self.matrix.append(submatrix)
        pass 



    def _lcm(self,a,b):
        '''
        Finds the LCM of the two leading terms of Polynomial a,b
        
        Params:
        a, b - polynomail objects
    
        returns:
        LCM - the np.array of the lead_term of the lcm polynomial
        '''
        return tuple(np.maximum(a.lead_term, b.lead_term))
    
    def calc_s(self,a,b,dec=9):
        '''
        Calculates the S-polynomial of a,b
        '''
        lcm = self._lcm(a,b)
        a_coeffs = np.zeros_like(a.coeff).astype('float')
        #idx = tuple([i-j for i,j in zip(lcm, a.lead_term)])
        #val = 1./(a.coeff[tuple(a.lead_term)])
        #TODO: Use attribute of poly for lead_term coeff
        a_coeffs[tuple([int(i-j) for i,j in zip(lcm, a.lead_term)])] = (a.coeff[tuple(a.lead_term)] * b.coeff[tuple(b.lead_term)])/(a.coeff[tuple(a.lead_term)])

        b_coeffs = np.zeros_like(b.coeff).astype('float')
        b_coeffs[tuple([int(i-j) for i,j in zip(lcm, b.lead_term)])] = (a.coeff[tuple(a.lead_term)] * b.coeff[tuple(b.lead_term)])/(b.coeff[tuple(b.lead_term)])

        if isinstance(a, MultiPower) and isinstance(b,MultiPower):
            b_ = MultiPower(np.round(b_coeffs,dec))
            a_ = MultiPower(np.round(a_coeffs,dec))
        elif isinstance(a, MultiCheb) and isinstance(b,MultiCheb):
            b_ = MultiCheb(np.round(b_coeffs,dec))
            a_ = MultiCheb(np.round(a_coeffs,dec))
        else:
            raise ValueError('Incompatiable polynomials')
        a1 = a_*a
        b1 = b_*b
        s = a_ * a - b_ * b
        if isinstance(a, MultiPower) and isinstance(b,MultiPower):
            s = MultiPower(np.round(s.coeff,dec))
        elif isinstance(a, MultiCheb) and isinstance(b,MultiCheb):
            s = MultiCheb(np.round(s.coeff,dec))
        else:
            raise ValueError('Incompatiable polynomials')
        return s

    def _coprime(self,a,b):
        '''
        a,b - ints

        Returns:
        True if a, b are coprime 
        False otherwise
        '''
        return fractions.gcd(a,b) == 1
    
    def add_s_to_matrix(self):
        '''
        This takes all possible combinaions of s polynomials and adds them to the Grobner Matrix
        '''
        for a, b in itertools.combinations(self.polys, 2):
            print('calculating s for a and b')
            submatrix = pd.DataFrame()
            if not self._coprime(a.lead_coeff,b.lead_coeff): #Checks for co-prime coeffs
                s = self.calc_s(a,b) # Calculate the S polynomail
                for idx in s.grevlex_gen():
                    idx_term = maxheap.TermOrder(tuple(idx)) # For each term in polynomial, throw it on the heap
                    if not idx_term.val in self.term_set: # Add all new polynomials
                        self.term_set.add(idx_term.val)
                        self.label.append(tuple(idx))
                        if idx_term > self.largest_mon:
                            self.largest_mon = idx_term
                    submatrix[str(idx)] = pd.Series([s.coeff[tuple(idx)]]) 
            self.matrix = self.matrix.append(submatrix)
            self.matrix = self.matrix.fillna(0)
            self.fs_len = len(self.matrix.index)
            pass

    def add_poly_to_matrix(self,p):
        submatrix = pd.DataFrame()
        for idx in p.grevlex_gen():
            submatrix[str(idx)] = pd.Series([p.coeff[tuple(idx)]])
        self.matrix = self.matrix.append(submatrix)
        self.matrix = self.matrix.fillna(0)
        pass

    def add_r_to_matrix(self):
        '''
        Makes Heap out of all monomials, and finds lcms to add them into the matrix
        '''
        for monomial in self.term_set:
            m = list(monomial)
            print(m)
            for p in self.polys:
                l = list(p.lead_term)
                if all([i<=j for i,j in zip(l,m)]) and len(l) == len(m):
                    c = [j-i for i,j in zip(l,m)]
                    c_coeff = np.zeros(np.array(self.largest_mon.val)+1)
                    c_coeff[tuple(c)] = 1 
                    if isinstance(p, MultiCheb):
                        c = MultiCheb(c_coeff)
                    elif isinstance(p,MultiPower):
                        c = MultiPower(c_coeff)
                    r = c*p
                    self.add_poly_to_matrix(r)
                    break
        pass 



