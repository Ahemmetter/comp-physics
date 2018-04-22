#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Die analytisch nicht lösbare Keplergleichung wird erst definiert und
dann numerisch über das Newton-Verfahren gelöst. Anschließend werden die
Bahnkurven der angegebenen Planeten in einem Polardiagramm geplottet.
Da man die Umlaufbahn der Erde praktisch nicht mehr sieht, sobald man
die des Pluto einblendet, hab ich eine alternative Darstellung mit einem
logarithmischen Radius eingebaut, so lassen sich die Umlaufbahnen aller
Himmelskörper gut erkennen."""

from __future__ import division
import scipy as sc #enthält bereits numpy
import scipy.optimize as opt
from matplotlib import pyplot as plt

erdjahr = 365 # Tage

"""Dictionary mit Parametern der Himmelskörper: Periode [d], numerische
Exzentrität, große Halbachse [AE], Farbe für den Plot, später dann noch
Arrays mit den Winkeln und den Radien (logarithmisch und normal). Die
Daten für die anderen Himmelskörper hab ich aus 
http://www.windows2universe.org/our_solar_system/planets_table.html"""

Planet = {"Erde": {"Periode": erdjahr, "numEx": 0.0167, "Halbachse": 1.0, "Farbe": "b"}, 
          "Pluto": {"Periode": 248*erdjahr, "numEx": 0.25, "Halbachse": 39.44, "Farbe": "k"},  
          "Halley": {"Periode": 76*erdjahr, "numEx": 0.97, "Halbachse":17.94, "Farbe": "k--"},
          "Merkur": {"Periode": 0.24*erdjahr, "numEx": 0.2056, "Halbachse": 0.39, "Farbe": "g"},
          "Venus": {"Periode": 0.62*erdjahr, "numEx": 0.0068, "Halbachse": 0.72, "Farbe": "c"},
          "Mars": {"Periode": 1.88*erdjahr, "numEx": 0.0934, "Halbachse": 1.52, "Farbe": "r"},
          "Jupiter": {"Periode": 11.86*erdjahr, "numEx": 0.0483, "Halbachse": 5.20, "Farbe": "y"},
          "Saturn": {"Periode": 29.46*erdjahr, "numEx": 0.056, "Halbachse": 9.54, "Farbe": "#cc2efa"},
          "Uranus": {"Periode": 84.01*erdjahr, "numEx": 0.0461, "Halbachse": 19.18, "Farbe": "#40ff00"},
          "Neptun": {"Periode": 164.8*erdjahr, "numEx": 0.0097, "Halbachse": 30.06, "Farbe": "#298a08"}}

def KeplerEq(E, eps, t, t0, T):
	""" Kepler-Gleichung."""
	return (E - eps*sc.sin(E) - 2*sc.pi*(t-t0)/T)

def KeplerEq_prime(E, eps, t, t0, T):
	""" 1. Ableitung der Kepler-Gleichung."""
	return 1 - sc.cos(E)*eps

def ex_Anom(planet, t=0, t0=0):
	""" Exzentrische Anomalie als Nullstelle der Kepler-Gleichung."""
	return opt.newton(KeplerEq, 3, KeplerEq_prime, args=(planet["numEx"], t, t0, planet["Periode"]))


def wahre_Anom(planet,t=0, t0=0):
	"""Wahre Anomalie wird aus exzentrischer Anomalie berechnet,
	Fallunterscheidung bei E => 180° und E <= 180°."""
	E = ex_Anom(planet,t)
	eps = planet["numEx"]
	if(E>=0 and E<=sc.pi):
		return sc.arccos((sc.cos(E)-eps)/(1-eps*sc.cos(E)))
	else:
		return 2*sc.pi-sc.arccos((sc.cos(E)-eps)/(1-eps*sc.cos(E)))

"""Berechnet den Radius von der Sonne zu jedem Zeitpunkt."""
def r(planet, theta, t=0, t0=0):
    eps = planet["numEx"]
    a = planet["Halbachse"]
    return a*((1 - eps**2)/(1 + eps*sc.cos(theta)))

for planet2 in Planet.keys():
	"""Baut Arrays mit Winkel und dazugehörigem Radius für jeden 
	Himmelskörper und legt alles unter einem neuen key im dictionary ab."""
	planet = Planet[planet2]
	theta_array = []
	r_array = []
	t_array = sc.linspace(0, planet["Periode"], 1000)
	for t in t_array:
		theta_array.append(wahre_Anom(planet, t))
		r_array.append(r(planet, theta_array[len(theta_array) - 1], t))
	planet["r"] = r_array
	planet["theta"] = theta_array

for planet2 in Planet.keys():
	"""Für die logarithmische Darstellung wird hier der Radius einfach
	logarithmiert; um negative Radii zu vermeiden, muss 1 dazuaddiert
	werden; damit beginnt auch die Log.skala bei 0 AE"""
	planet = Planet[planet2]
	r_log_array = []
	for i in range(0, 1000):
		r_log_array.append( sc.log(Planet[planet2]["r"][i]+1) )
	planet["r_log"] = r_log_array

def showplot(logmode):
	"""Kleine Funktion, die erst abfragt, ob man eine logarithmische
	oder "normale" Skala haben will und dann über das dictionary iteriert
	und alle Bahnkurven plus Legende und Titel erstellt."""
	if logmode == "yes":
		for planet2 in Planet.keys():
			plt.polar(Planet[planet2]["theta"], Planet[planet2]["r_log"], Planet[planet2]["Farbe"], label = str(planet2))
			plt.legend(loc="lower left", prop={'size':7})
			plt.suptitle("Logarithmische Skala", fontsize=12)
	else:
		for planet2 in Planet.keys():
			plt.polar(Planet[planet2]["theta"], Planet[planet2]["r"], Planet[planet2]["Farbe"], label = str(planet2))
			plt.legend(loc="lower left", prop={'size':7})
			plt.suptitle("Normale Skala", fontsize=12)
	plt.show()

logmode = raw_input("Logarithmische Skala? (yes/no):  ")
showplot(logmode)
