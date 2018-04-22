#!/usr/bin/python
#-*- coding: utf-8 -*-

"""Durch Anwendung der Mittelpunkt-, Trapez- und Simpsonregeln wird das
bestimmte Integral einer gegebenen Funktion berechnet.
Integrationsgrenzen und Anzahl der Stützstellen sind in der erstellten
Funktion als Parameter anzugeben.
Im zweiten Teil wird das Ergebnis mit den Resultaten der eingebauten
scipy-Funktion scipy.integrate verglichen.
Zuletzt soll f(x) geplottet werden."""

import scipy as sc #enthält bereits math und numpy
from matplotlib import pyplot as plt
import scipy.integrate as integ

def f(x):
	"""Angegebene Funktion, von der das Integral berechnet werden soll."""
	return (sc.log(x**2+5)*sc.cos(0.8*x)+3.5*x)/(sc.e**(x/10))


def integral(f,s,a,b):
	"""
	Selbstgeschriebene Funktion, die auf 3 verschiedene Arten das
	bestimmte Integral einer gegebenen Funktion berechnet. Die Funktion
	übernimmt die Funktion (also f(x)), Stützpunktanzahl, obere und 
	untere Grenze als Parameter und berechnet daraus über die 
	Mittelwertsregel, die Trapezregel und die Simpsonregel jeweils das 
	Integral.
	"""
	x = sc.linspace(a,b,s)
	h = x[1]-x[0] #Schrittweite
	
	int_mitt_array = []
	for i in range(0,s-1):
		int_mitt_array.append(f((x[i+1]+x[i])/2.))	
	int_mitt = h * sc.sum(int_mitt_array)
	print "Mittelwertsregel mit " + str(s) + " Stützpunkten:   " + str(int_mitt)
	
	int_trapz_array = []
	for i in range(0,s-1):
		int_trapz_array.append(((f(x[i+1]))+(f(x[i])))/2.)
	int_trapz = h * sc.sum(int_trapz_array)
	print "Trapezregel mit " + str(s) + " Stützpunkten:   " + str(int_trapz)
	
	int_simps_array = []
	for i in range(0,s-1):
		int_simps_array.append((1/6.)*((f(x[i]))+4*(f((x[i]+x[i+1])/2))+f(x[i+1])))
	int_simps = h * sc.sum(int_simps_array)
	print "Simpsonregel mit " + str(s) + " Stützpunkten:   " + str(int_simps)
	
	integral_man = [int_mitt, int_trapz, int_simps]
	return integral_man


def scintegral(f,s,a,b):
	"""Die Funktion benutzt die eingebauten Funktionen integ.trapz,
	integ.simps und integ.quad, um das Integral einer gegebenen Funktion
	zu bestimmen. Die Funktion übernimmt, wie auch die von oben, die
	Funktion, Stützpunktanzahl, obere und untere Grenze."""
	x = sc.linspace(0,10,1000)
	i_trapez = integ.trapz(f(x), x)
	i_simpson = integ.simps(f(x), x)
	i_quad = integ.quad(f, 0, 10)
	i_quad2 = i_quad[0]
	
	print "integ.trapz() bei " + str(s) + " Stützpunkten:   " + str(i_trapez)
	print "integ.simps() bei " + str(s) + " Stützpunkten:   " + str(i_simpson)
	print "integ.quad() bei " + str(s) + " Stützpunkten:   " + str(i_quad2)
	
	integral_pre = [i_quad2, i_trapez, i_simpson]
	return integral_pre


def compare_int(f, s, a, b):
	"""Funktion berechnet Differenz zwischen berechneten Integralen."""
	integral_comp = []
	integral_array = integral(f,s,a,b)
	scintegral_array = scintegral(f,s,a,b)
	for i in range(1,3):
		"""Da ich mir nicht sicher war, ob man integ.quad und die
		Mittelwertsregel vergleichen kann, hab ich das weggelassen."""
		integral_comp.append(integral_array[i] - scintegral_array[i])
	print "Abweichung bei Trapezregel:  " + str(integral_comp[0])
	print "Abweichung bei Simpsonregel:  " + str(integral_comp[1])


compare_int(f, 10,   0, 10)
print "..."*5
compare_int(f, 100,  0, 10)
print "..."*5
compare_int(f, 1000, 0, 10)


"""Im letzten Teil der Aufgabe soll die gegebene Funktion geplottet
werden. Als Veranschaulichung für das Integral als Fläche unter dem
Graphen habe ich diese eingefärbt. Auch ist der geplottete Ausschnitt 
(-2, 12) ein größerer als der zwischen den Integrationsgrenzen (0, 10)."""
x2 = sc.linspace(-2., 12., 1000)
plt.plot(x2, (sc.log((x2**2)+5)*sc.cos(0.8*x2)+(3.5*x2))/(sc.e**(x2/10)), 'r')
plt.ylabel('f($x$)')
plt.xlabel('$x$')
plt.grid()
plt.text(5, -5, r'$f(x) = \frac{\ln(x^2+5) \cos(0.8x)+3.5x}{e^{\frac{x}{10}}}$', fontsize=20)
"""In der Beschriftung kann man LaTeX-Code benutzen, um mathematische
Ausdrücke sauber zu rendern."""
plt.fill_between(x2,(sc.log((x2**2)+5)*sc.cos(0.8*x2)+(3.5*x2))/(sc.e**(x2/10)), 0, color='blue', alpha = 0.2)
plt.show()
