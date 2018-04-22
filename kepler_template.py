#!/usr/bin/python                 # python - Interpreter
# -*- coding: utf-8 -*-           # Sonderzeichen und deutsche Umlaute
from __future__ import division  # problemlose Ganzzahl-Division
import scipy as sc               # scipy beinhaltet numpy
import scipy.optimize as opt     # Funktionen für Nullstellensuche
from matplotlib import pyplot as plt
"""
Nullstellensuche: Kepler-Problem
"""
erdjahr = 365 # Tage
# Parameter der Himmelskörper (Periode [d], numerische Exzentrizität und
# große Halbachse [AE]):
Planet = {"Erde": {"Periode": erdjahr, "numEx": 0.0167, "Halbachse": 1.0}, 
          "Pluto": {"Periode": 248*erdjahr, "numEx": 0.25, "Halbachse": 39.44},  
          "Halley": {"Periode": 76*erdjahr, "numEx": 0.97, "Halbachse":17.94} }

def KeplerEq(E, eps, t, t0, T):
    """ Kepler-Gleichung """
    return ...

def KeplerEq_prime(E, eps, t, t0, T):
    """ 1. Ableitung der Kepler-Gleichung """
    return ...

def ex_Anom(planet, t=0, t0=0):
    """ Exzentrische Anomalie als Nullstelle der Kepler-Gleichung """
    return opt.newton( ... )

# Weiter mit Berechnung der wahren Anomalie und des Abstandes von der Sonne:
