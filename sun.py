#-*- coding: utf-8 -*-

import scipy as sc #enthält bereits math und numpy
from matplotlib import pyplot as plt

def H(L, D):
	return abs((1/15.0)*sc.arccosh(-sc.tan(sc.radians(L)) * sc.tan(sc.radians(23.44)*sc.sin(sc.radians(((D+284)*360)/365.0)))))

D = 105
L = -40
#print "Sunrise: " + str(H(L, D))

print str(-sc.arccosh(L*(sc.pi/180)) * sc.tan(23.44*(sc.pi/180)*sc.sin((((D+284)*360)/365.0)*(sc.pi/180))))

"""
x2 = sc.linspace(-2., 12., 1000)
plt.plot(x2, (sc.log((x2**2)+5)*sc.cos(0.8*x2)+(3.5*x2))/(sc.e**(x2/10)), 'r')
plt.ylabel('f($x$)')
plt.xlabel('$x$')
plt.grid()
plt.text(5, -5, r'$f(x) = \frac{\ln(x^2+5) \cos(0.8x)+3.5x}{e^{\frac{x}{10}}}$', fontsize=20)
plt.fill_between(x2,(sc.log((x2**2)+5)*sc.cos(0.8*x2)+(3.5*x2))/(sc.e**(x2/10)), 0, color='blue', alpha = 0.2)
plt.show()
"""
