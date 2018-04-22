#-*- coding: utf-8 -*-

"""Plottet Bahnkurve aus ExPhy-Aufgabe 2.4 mit matplotlib"""

import numpy as np
from matplotlib import pyplot as plt

"""Startwerte und Konstanten"""
v0 = 14.0 #Anfangsgeschwindigkeit
z0 = 2.45 #Anfangshöhe
g = 9.81 #Fallbeschleunigung
m = 7.257 #Masse des Wurfkörpers

"""Berechnet optimalen Abwurfwinkel"""
alpha = np.arctan(v0/np.sqrt(v0**2 + 2*g*z0))

"""Berechnet Nullstelle der Trajektorie"""
x1 = (-np.tan(alpha)-np.sqrt((np.tan(alpha)**2)-4.0*(-(g/2)*(1./v0**2)*(1.+np.tan(alpha)**2)*z0)))/(2.*(-(g/2)*(1./v0**2))*(1.+np.tan(alpha)**2))

"""Einteilung der x-Achse"""
x = np.linspace(0., x1, 1000)

"""Berechnet Wurfweite"""

wurfweite = np.max(x) - 0
print "Die Wurfweite beträgt " + str(wurfweite) +"m."

"""Berechnet Koordinaten des höchsten Punkts"""

z = -(g/2)*(x**2/v0**2)*(1+np.tan(alpha)**2)+x*np.tan(alpha)+z0

z_hoechsterPunkt = np.max(z) #z-Koordinate

i = 0
for i in range(0,1000):
	if z[i] == np.max(z):
		position=i

x_hoechsterPunkt = x[position] #x-Koordinate

print "Die Koordinaten des höchsten Punktes sind " + str(x_hoechsterPunkt) + ", " + str(z_hoechsterPunkt) + "."

"""Plottet potentielle Energie einer Kugel mit Masse m und Bahnkurve aus Aufgabe 1"""

ax1 = plt.plot(x, -(g/2)*(x**2/v0**2)*(1.+np.tan(alpha)**2)+x*np.tan(alpha)+z0, 'r')
#Trajektorie der Kugel
plt.ylabel('z in m')
ax2 = plt.twinx()
plt.plot(x, z*g*m, 'b')
#Potentielle Energie der Kugel
plt.ylabel('Epot in J')
plt.show()
