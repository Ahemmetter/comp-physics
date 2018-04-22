#!/usr/bin/python
#-*- coding: utf-8 -*-

"""Integriert und plottet beliebige Funktion numerisch."""

import scipy as sc
from matplotlib import pyplot as plt
import scipy.integrate as integ

limits = [0, 1, 1000]

def f(x):
	return sc.sin(x) * x**2

def getLimits():
	limits[0] = float(raw_input("von:  "))
	limits[1] = float(raw_input("bis:  "))
	stpkt = raw_input("Stützpunkte:  ")
	if type(stpkt) != type(0.3) or type(stpkt) != type(2):
		limits[2] = 1000
	else:
		limits[2] = float(stpkt)
	return limits

def integral(f,limits):
	x = sc.linspace(limits[0], limits[1], limits[2])
	print integ.trapz(f(x), x)

def plot(f, limits):
	x = sc.linspace(limits[0], limits[1], limits[2])
	spanne = limits[1] - limits[0]
	x2 = sc.linspace(limits[0]-spanne*0.1, limits[1]+spanne*0.1, limits[2])
	plt.plot(x2, f(x2), 'r')
	plt.ylabel('$f(x)$')
	plt.xlabel('$x$')
	plt.grid()
	plt.fill_between(x,f(x), 0, color='blue', alpha = 0.2)
	plt.show()

def menu():
	wish = "p"
	while wish != "q":
		wish = raw_input("Integration (i), Plot (p), beides (b) oder schließen (q)?  ")
		if wish == "i":
			getLimits()
			integral(f,limits)
		elif wish == "p":
			getLimits()
			plot(f, limits)
		elif wish == "b":
			getLimits()
			integral(f, limits)
			plot(f, limits)
		elif wish == "q":
			break
		else:
			print "Error"

menu()
