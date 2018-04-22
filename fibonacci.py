#!/usr/bin/python                # python - Interpreter 
# -*- coding: utf-8 -*-          # Sonderzeichen und deutsche Umlaute
from __future__ import division  # problemlose Ganzzahl-Division
import math, time                # grundlegende Mathematik-Funktionen

""" 3. Übung - Aufgabe 3
	Dieses Programm enthält die Funktionen reFibonacci(n),
	itFibonacci(n), testitFibonacci und testreFibonacci. Die ersten
	beiden übernehmen je einen Wert als Ordung und berechnen die dieser
	Ordnung zugewiesene Fibonacci Zahl. Dies erfolgt bei reFibonacci(n)
    durch Rekursion und bei itFibonacci(n) durch Iteration.
	testreFibonacci testet reFibonacci(n) für n = {10,20,30,40}
	testitFibonacci erstellt eine Liste für die ersten 50 Fibonacci-
	-Zahlen.
	Das Hauptprogramm enthält eine Menüführung durch die man die
	unterschiedlichen Funktionen aufrufen kann. Dazu wird zwischen den
	möglichen Angaben: r, i, tr, ti und a unterschieden. a Beendet das
	Programm
"""
x = 0	# globale Variable um die Rekursionen von reFibonacci(n) zu
		# zählen

def reFibonacci(n):
	""" Die Funktion reFibonacci(n) berechnet durch Rekursion die
		Fibonacci Zahl zur angegebenen Ordnung.
		Die Variable x wird dabei zum Zählen der Rekursionen verwendet.
		Dabei ist zu erkennen, dass für n+1 die Anzahl der Rekursionen
		um das ca 1,7 fache ansteigt. Das wirkt sich genauso auf die
		Berechnungszeit aus. Diese steigt so exponentiell an.
		Eingabe: eine Natürliche Zahl (mit 0)
		Ausgabe: die zugehörige Fibonacci Zahl
	"""
	global x
	x += 1

	if n == 0:
		return 0
	if n == 1:
		return 1
	else:
		return reFibonacci(n-1) + reFibonacci(n-2)

def itFibonacci(n):
	""" Die Funktion itFibonacci(n) berechnet Iteration die
		Fibonacci Zahl zur angegebenen Ordnung.
		Eingabe: eine Natürliche Zahl (mit 0)
		Ausgabe: die zugehörige Fibonacci Zahl
	"""
	if(n != 0):
		x = 0
		y = 1
		for i in range(n-1):
			i += 1
			z = x + y
			x = y
			y = z
		return y
	else:
		return 0

def testreFibonacci():	
	""" Die Funktion testreFibonacci berechnet zu den Ordnungen 10, 20,
		30 und 40, je die Fibonacci Zahl mit Hilfe der Funktion
		reFibonacci(n). Dazu wird die zur Berechnung nötige Zeit
		und die Anzahl der Rekursionen ausgegeben.
		Eingabe: -
		Ausgabe: Tabelle mit Ordnungen, Fibonacci Zahlen, Anzahl der
				 Funktionsaufrufe und Berechnungszeit.
	"""
	print "Fibonacci Zahlen folgender Ordnungen sind: \n\n"
	print "Ordnung\tFibonacci-Zahl\tZeit zur Berechnung\tAnzahl der Funktionsaufrufe\n", 75*"-"

	ls = [10,20,30,40]
	lf = []
	lt = []
	l= 0
	for i in ls:
		x = 0
		t1 = time.time()
		lf.append(reFibonacci(i))
		lt.append(round(time.time()-t1,5))
		print "  ",i, "{0:14}".format(lf[l]), "{0:16}".format(lt[l]), "s\t", "{0:25}".format(x)
		l += 1

def testitFibonacci():
	""" Die Funktion testitFibonacci berechnet zu den Ordnungen 0-50,
		je die Fibonacci Zahl mit Hilfe der Funktion
		itFibonacci(n). Dazu wird das Verhältnis zum Vorgänger mit 50
		Dezimalstellen angegeben
		Eingabe: -
		Ausgabe: Tabelle mit Ordnungen, Fibonacci Zahlen, Verhältnisse
				 zum jeweiligen Vorgänger
	"""
	print "Ordnung\tFibonacci-Zahl\tVerhältnis zum Vorgänger\n", 75*"-"
	for i in range(1,51):
		if itFibonacci(i-1) != 0:
			v = itFibonacci(i)/itFibonacci(i-1)
		else:
			v = 1
		print "{0:3}".format(i), "{0:16}".format(itFibonacci(i)), "\t",  # 1. Menüpunkt

# Hauptprogramm Menüführung
print "Programm zur Berechnung von Fibonacci-Zahlen beliebiger Ordnung\n"
print 80*"-", "\nr:  Berechnung durch Rekursion mit Zeit und Anzahl-Angabe\n"
print "i:  Berechnung durch Iteration, mit Angabe des Verhältnisses zum Vorgänger\n"
print "tr: Ausgabe einer durch Rekursion erzeugten Tabelle mit Zeiten\n    und Rekursionsanzahl für 4 Ordnungen\n"
print "ti: Ausgabe einer durch Iteration erzeugten Tabelle mit Verhältnissen\n    zum Vorgänger\n"
print "a:  Abbruch\n", 80*"-"	   

# Schleife, die beliebig oft Befehle des Nutzers ausführt
while True:
	
	print "\n\nNeuer Befehl (r, i, tr, ti, a) . . ."
	f = raw_input() # zur Wahl des Menüpunkts
	
	if f != 'a':
		if f == 'r': # 1. Menüpunkt
			u = input("Geben Sie eine Ordnung an: ")
			t1 = time.time()
			y = reFibonacci(u)
			w = round(time.time()-t1, 5)
			print "\nOrdnung\tFibonacci-Zahl\tZeit zur Berechnung\tAnzahl der Funktionsaufrufe\n"
			print "  ",u, "{0:14}".format(y), "{0:16}".format(w), "s\t", "{0:25}".format(x)
	
		elif f == 'i': # 2. Menüpunkt
			u = input("Geben Sie eine Ordnung an: ")
			y = itFibonacci(u)
			v = y/itFibonacci(u-1)
			print "\nOrdnung\tFibonacci-Zahl\tVerhältnis zum Vorgänger\n"
			print "{0:3}".format(u), "{0:16}".format(y), "\t", format(v, '.50f')
			
		elif f == 'tr': # 3. Menüpunkt
			testreFibonacci()
			
		elif f == 'ti': # 4. Menüpunkt
			testitFibonacci()
	else:
		
		print "\nEnde des Programms"
		break

