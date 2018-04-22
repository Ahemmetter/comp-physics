#-*- coding: utf-8 -*-

"""Berechnet Fakultät zu beliebiger Ordnung"""
import math
from decimal import Decimal

def Fakultaet(n):
	"""Übernimmt Parameter n (Ordnung) und berechnet daraus die
	Fakutät. Für 0 und 1 ist ein Startwert vorgegeben. Ebenso wird die
	Eingabe überprüft, ob es sich bei dieser um einen integer handelt."""
	if type(n) != type(1): return "Eingabe ist keine natürliche Zahl"
	elif n == 0 or n == 1: return n
	else: return math.factorial(n)
	
n=10
print Fakultaet(n)


def Euler(zahl):
	"""Approximiert die Eulersche Zahl e durch Iteration."""
	i = 1
	e = 1
	while i <= zahl:
		e= e+(1./Fakultaet(i))
		i = i+1
	return Decimal(e)
	
zahl = 10
print Euler(zahl)

zahl = 100
print Euler(zahl)

zahl = 150
print Euler(zahl)

zahl = 200
print Euler(zahl) #gibt overflow error, anscheinend Ziel dieser Übung.
