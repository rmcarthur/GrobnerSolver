from __future__ import division, print_function
import numpy as np
from scipy.signal import fftconvolve, convolve
import itertools

"""
08/31/17
Author: Rex McArthur
Creates a class of n-dim chebyshev polynomials. Tracks leading term,
coefficents, and inculdes basic operations (+,*,scaler multip, etc.)
Assumes GRevLex ordering, but should be extended.
"""


class MultiCheb(object):
    """
    _____ params _______
    dim: int, number of variables, dimension of chebyshev system
    terms: int, highest term of single variable chebyshev polynomials
    coeff: list(terms**dim) or np.array ([terms,] * dim), coefficents in given ordering 
    order: string, monomial ordering desired for Grubner calculations
    lead_term: list, the index of the current leading coefficent



    _____ methods ______
    next_step:
        input- Current: list, current location in ordering
        output- the next step in ordering
    """

    def __init__(self, coeff, order='grevlex', lead_term=None):
        '''
        terms, int- number of chebyshev polynomials each variable can have. Each dimension will have term terms
        dim, int- number of different variables, how many dim our tensor will be
        order, string- how you want to order your polynomials. Grevlex is default
        '''
        self.coeff = coeff
        self.dim = self.coeff.ndim
        self.terms = np.prod(self.coeff.shape)
        self.order = order
        self.shape = self.coeff.shape
        self.max_term = np.max(self.shape) -1

        if lead_term is None:
            self.update_lead_term()
        else:
            self.lead_term = lead_term


    def next_step(self, current):
        '''
        Used to calculate next step in the grevlex generator
        '''
        for i in range(self.dim-1, 0, -1):
            i = int(i)
            if i!= self.dim-1 and current[i] == 0:
                break
            elif i!= 0 and  current[i] < self.max_term and current[i-1] > 0:
                current[i] += 1
                current[i-1] -= 1
                return current

        if len(current.nonzero()) > 0:
            ##### This is the problem ######
            first_z = -1 * next(j for j,v in enumerate(current[::-1]) if v==0) - 1
            # Finds the first non-zero afte a zero and iterates from there to create the 
            # Next high state
            first_nz_after_z = -1*next(i for i,v in enumerate(current[first_z::-1]) if v!=0) -1
            j = first_z + first_nz_after_z + 1
            current[j] -= 1
            current[j+1:] = self._calc_high_state(current[j+1:], self.state_sum-np.sum(current[:j+1]))
            return current
        raise ValueError("Condition not covered in step func")

    def grevlex_gen(self, current=None):
        '''
        yields grevlex ordering co-ordinates in order to find 
        the leading coefficent
        '''
        self.state_sum = sum(np.array(self.shape)-1)
        if current == None:
            current = np.array(self.shape) -1
        low_state = self._calc_low_state(current)
        self.state_sum = np.sum(current)
        last_i = np.zeros_like(current)
        last_i[-1] = 1
        yield current
        while True:
            if all(current == last_i):
                yield np.zeros_like(current)
                return
            elif all(current == low_state):
                #print('Current -- lw_state')
                #print('State Sum: {}'.format(self.state_sum))
                #raw_input()
                self.state_sum -= 1
                current = self._calc_high_state(current, self.state_sum)
                low_state = self._calc_low_state(current)
                yield current
            else: 
                current = self.next_step(current)
                yield current

    def _calc_low_state(self,current):
        max_term = np.max(self.shape) -1
        if self.state_sum < max_term:
            low_state = np.zeros_like(current)
            low_state[-1] = self.state_sum
            return low_state
        else:
            #print('State sum: {}'.format(self.state_sum))
            #print('terms: {}'.format(self.dim))
            #print(self.shape)
            #raw_input()
            slots = int(self.state_sum//max_term)
            remainder = self.state_sum % max_term
            low_state = np.zeros_like(current)
            low_state[-slots:] = (self.shape[0]-1)*np.ones(1)
            if remainder != 0:
                low_state[-slots - 1] = remainder
            return low_state.astype(int)

    def _calc_high_state(self, current, sum_val):
        max_term = np.max(self.shape) -1
        slots = int(sum_val//max_term)
        remainder = sum_val % max_term
        high_state = np.zeros_like(current)
        high_state[:slots] = (max_term)*np.ones(1)
        if remainder != 0:
            high_state[slots] = remainder
        return high_state.astype(int)

    def update_lead_term(self,start = None):
        #print('Updating Leading Coeff...')
        if self.order == 'grevlex':
            gen = self.grevlex_gen()
            for idx in gen:
                if self.coeff[tuple(idx)] != 0:
                    self.lead_term = idx
                    self.lead_coeff = self.coeff[tuple(idx)]
                    break
        #print('Leading Coeff is {}'.format(self.lead_term))


    def __lt__(self, other):
        '''
        Magic method for determing which polynomial is smaller
        '''
        if sum(self.lead_term) < sum(other.lead_term):
            return True

        elif sum(self.lead_term) > sum(other.lead_term):
            return False
        
        else:
            for i in xrange(len(self.lead_term)):
                if self.lead_term[i] < other.lead_term[i]: 
                    return True
                if self.lead_term[i] > other.lead_term[i]:
                    return False
            if self.coeff[tuple(self.lead_term)] < other.coeff[tuple(other.lead_term)]:
                return True


    def __gt__(self, other):
        '''
        Magic method for determing which polynomial is smaller
        '''
        if sum(self.lead_term) < sum(other.lead_term):
            return False

        elif sum(self.lead_term) > sum(other.lead_term):
            return True
        
        else:
            for i in xrange(len(self.lead_term)):
                if self.lead_term[i] < other.lead_term[i]: 
                    return False
                if self.lead_term[i] > other.lead_term[i]:
                    return True
            if self.coeff[tuple(self.lead_term)] < other.coeff[tuple(other.lead_term)]:
                return False

    def __add__(self,other):
        '''
        Here we add an addition method 
        '''
        return MultiCheb(self.coeff + other.coeff)

    def __sub__(self,other):
        '''
        Here we subtract the two polys coeffs
        '''
        return MultiCheb(self.coeff - other.coeff)


    def match_size(self,a,b):
        '''
        Matches the size of the polynomials
        '''
        new_shape = [max(i,j) for i,j in itertools.izip_longest(a.shape, b.shape)]
        add_a = [i-j for i,j in zip(new_shape, a.shape)]
        add_b = [i-j for i,j in zip(new_shape, b.shape)]
        add_a_list = np.zeros((2,len(new_shape)))
        add_b_list = np.zeros((2,len(new_shape)))
        add_a_list[:,1] = add_a
        add_b_list[:,1] = add_b
        a = MultiCheb(np.pad(a.coeff,add_a_list.astype(int),'constant'))
        b = MultiCheb(np.pad(b.coeff,add_b_list.astype(int),'constant'))
        return a,b

    def __mul__(self,other):
        '''
        Multiply by convolving intelligently
        CURRENTLY ONLY DOING 2-D support
        Manually make 1, 3D support then add n-dim support
        '''
        # Check and see if same size
        if self.shape != other.shape:
            new_self, new_other = self.match_size(self,other)
        else:
            new_self, new_other = self, other
        c = new_other.coeff[::-1, ::-1]
        p1 = convolve(new_self.coeff,new_other.coeff)
        temp = convolve(new_self.coeff,c)
        half = len(p1)//2
        p2 = temp[:half+1,:][::-1] + temp[half:,:]
        p2[0,:] = p2[0,:]/2.
        p2 = p2[:,:half+1][:, ::-1] + p2[:,half:]
        p2[:,0] = p2[:,0]/2.
        p_z = np.zeros_like(p1)
        p_z[:half+1, :half+1] = p2
        new_coeff = .5*(p1 + p_z)
        #TODO: You can use the lead_term kwarg to save some time
        return MultiCheb(new_coeff)

