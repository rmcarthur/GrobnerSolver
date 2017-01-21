from __future__ import division, print_function
import numpy as np
import math
from scipy.fftpack import dct, idct
from numpy.fft import ifftn, fftn
from numpy.polynomial import chebyshev as cheb
from scipy.signal import convolve, fftconvolve

def con_mult(a,b):
    c = b[::-1]
    p1 = convolve(a,b)
    temp = convolve(a,c)
    half = len(p1)//2
    p2 = temp[:half+1][::-1] + temp[half:]
    p2[0] = p2[0]/2
    p_z = np.zeros_like(p1)
    p_z[:half+1] = p2
    return .5*(p1 + p_z)
    #pass

def con_mult_2d(a,b):
    #Assuming a square tensor
    c = b[::-1, ::-1]
    p1 = convolve(a,b)
    temp = convolve(a,c)
    half = len(p1)//2
    p2 = temp[:half+1,:][::-1] + temp[half:,:]
    p2[0,:] = p2[0,:]/2.
    p2 = p2[:,:half+1][:, ::-1] + p2[:,half:]
    p2[:,0] = p2[:,0]/2.
    p_z = np.zeros_like(p1)
    p_z[:half+1, :half+1] = p2
    return .5*(p1 + p_z)

def con_mult_nd(a,b):
    if a.ndim != b.ndim:
        raise ValueError('Number of Dimensions do not match')
    dim = a.ndim
    #Flip each dim,
    p1 = convolve(a,b)
    temp = convolve(a,c)
    half = len(p1)//2
    p2 = temp[:half+1,:][::-1] + temp[half:,:] #TODO: Change this for each dim
    p2[0,:] = p2[0,:]/2.
    p2 = p2[:,:half+1][:, ::-1] + p2[:,half:] #TODO: Change this for each dim
    p2[:,0] = p2[:,0]/2. 
    p_z = np.zeros_like(p1)
    p_z[:half+1, :half+1] = p2
    return .5*(p1 + p_z)




a = np.array([[1,2,3],
    [4,5,6],
    [3,2,1]])
b = np.array([[1,1,2],
    [3,1,2],
    [4,1,2]])
###
print(con_mult_2d(a,b))
test1 = np.array([[0,1],[2,1]])
test2 = np.array([[2,2],[3,0]])

#t1 = np.array([3.5,2, .5])
#t2 = np.array([9,2, 2])
print(con_mult_2d(test1, test2))
truth = np.array([[4, 3.5, 1],[5,9,1],[3,1.5,0]])
print('Truth: \n{}'.format(truth))
