#!/usr/bin/python
# -*- coding: utf-8 -*-q

from __future__ import division
import numpy as np
from matplotlib import pyplot as plt

def diff(x, t):
    """ Bildet die Ableitung eines Arrays x mit den absoluten Zeiten t
    """
    size = x.size
    #listcomprehension vom 1. bis size-2. element
    #mittels zentraler Differenziation
    ret = [(x[i+1] - x[i-1])/(t[i+1] - t[i-1]) for i in xrange(1, size - 1)]
    first = [(x[1] - x[0]) / t[1]] # forwärtsdifferentiation
    # anhängen des letzten elementes (durch rückwärsdifferentiation)
    ret.append((x[size - 1] - x[size - 2]) / (t[size-1] - t[size-2]))
    first.extend(ret) # kombinieren des 1. elements mit allen anderen
    return first
    

t, x, z = np.loadtxt("Bewegung.dat", skiprows=1, unpack = True)
m = 7.257 # kg
g = 9.81 # m / s²

# geschwindigkeit über pythagoras mit den ableitungen nach x und z
v = np.sqrt(np.array(diff(x, t))**2 + np.array(diff(z, t))**2)

fig = plt.figure("Energiediagramme für diskrete Wertetabelle eines schrägend Wurfes")

plt.subplot(211)
plt.title("Energien mit eigener Ableitung")
plt.plot(t, 1/2 * m * v**2, "b-") # e_kin
plt.plot(t, m * g * z, "g-") # e_pot
plt.plot(t, m * g * z + 1/2 * m * v**2, "y-") #e_gesamt
plt.legend((r"$E_{kin}$", r"$E_{pot}$", r"$E_{ges}$"), loc=7)
plt.grid(True)
plt.xlabel(r"$Zeit  [T]=1s$")
plt.ylabel(r"$Energie  [E]=1J$")
plt.axis([0, 2.2, 0, 1000])

#delta t zwischen jeden zeiten
dt = [t[i+1] - t[i] for i in xrange(0, x.size - 1)]
dt.append(t[t.size-1] - t[t.size-2])
dt = np.around(dt, 2)
 
vx = np.gradient(x, dt)
vz = np.gradient(z, dt)

plt.subplot(212)
plt.title("Energien durch Ableitung mit numpy")
plt.plot(t, 1/2 * m * np.sqrt(vx**2 + vz**2)**2, "b-") # e kin
plt.plot(t, m * g * z, "g-") # e pot
plt.plot(t, m * g * z + 1/2 * m * np.sqrt(vx**2 + vz**2)**2, "y-") # e gesamt
plt.legend((r"$E_{kin}$", r"$E_{pot}$", r"$E_{ges}$"), loc=7)
plt.grid(True)
plt.xlabel(r"$Zeit  [T]=1s$")
plt.ylabel(r"$Energie  [E]=1J$")
plt.axis([0, 2.2, 0, 1000])

plt.show()
