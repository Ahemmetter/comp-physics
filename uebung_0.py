#!/usr/bin/python       #Header
# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt


"""
Dieses Programm gibt eine Spirale aus, die der Parametrisierung
r(t) = (1/2)**(t)
\phi(t) = 2 * np.pi * t
"""

def spirale(x=0 , y=0):
	"""Dieses Programm generiert Spiralkoordinaten
	"""
	t = np.linspace(0.0, 5, 500)
	x = (0.5) ** (t) * np.cos(2 * np.pi * t) + x
	y = (0.5) ** (t) * np.sin(2 * np.pi * t) + y
	return x , y
	
print spirale()


def wenn_maus_klick(event):
	plt.plot(spirale(event.xdata, event.ydata)[0] ,spirale(event.xdata, event.ydata)[1])
	plt.draw()
	print event.xdata , event.ydata	
	
	
#Hauptprogramm

plt.plot(spirale()[0],spirale()[1])
plt.connect('button_press_event', wenn_maus_klick)
plt.show()





