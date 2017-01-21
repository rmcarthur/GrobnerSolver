from __future__ import division
import numpy as np
import multiplication as mult
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy.polynomial import chebyshev as cheb

def f1(X,Y):
    return .1*X**2 + .2*X - 4 + .2*Y**2 - .6*Y

def f2(X,Y):
    return -.3*X**2 + X - 4 + .6*Y**2 - .6*Y

def plot(X,Y,Z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(X,Y,Z1)
    plt.show()
    pass


y = np.linspace(-1,1,100)
x = np.linspace(-1,1,100)
#a = cheb.Chebyshev([3.5,3,.5])
#b = cheb.Chebyshev([9,2,2])
#abc = a*b
#ab = cheb.Chebyshev([34, 27.5, 13.5, 2.5, 0,5])
#plt.plot(x, cheb.chebval(x,a.coef))
#plt.plot(x, cheb.chebval(x,b.coef))
#plt.plot(x, cheb.chebval(x,ab.coef))
#plt.plot(x, cheb.chebval(x,abc.coef))
#plt.show()
#


F1_mat = np.array([[-4, .2, .1],[-4, -.6, .2]])

X,Y = np.meshgrid(x,y)
Z1 = f1(X,Y)
Z2 = f2(X,Y)
fig1 = plt.figure()
fig2 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax2 = fig2.add_subplot(111, projection='3d')

ax1.plot_surface(X,Y,Z1)
ax2.plot_surface(X,Y,Z2)
plt.show()

Z3 = Z1*Z2
fig3 = plt.figure()
ax3 = fig3.add_subplot(111,projection='3d')
ax3.plot_surface(X,Y,Z3)
plt.show()










z4 = cheb.chebval2d(x,y, F1_mat)
print(z4.size)
fig4 = plt.figure()
ax4 = fig4.add_subplot(111,projection='3d')
ax4.plot_surface(x,y,z4)
plt.show()
#chebz = cheb.chebgrid2d(x,y)
x1_pol = [-4, .2, .1]
y1_pol = [0, -.6, .2]
#
#x1_cheb = cheb.cheb2poly(x1_pol)
#y1_cheb = cheb.cheb2poly(y1_pol)
#cheb_X = cheb.chebval(-5, x1_cheb)
#cheb_Y = cheb.chebval(-5, y1_cheb)
#p_X = fx1(X)
#p_Y = fy1(Y)
#print(cheb_X)
#print(cheb_Y)
#print(p_X)
#print(p_Y)
#
#
#def f1_cheb(fx, fy, X,Y):
#    return cheb.chebval(X,fx) + cheb.chebval(Y,fy)
#    
#Z_cheb = f1_cheb(x1_cheb, y1_cheb, X,Y)
#ax2.plot_surface(X,Y,Z_cheb)
#
#plt.show()
