#-*- coding: utf-8 -*-
"""Berechnet das Volumen einer Kugel bei gegebenem Radius r.
"""

#zu senden an k.steiniger@hzdr.de
import math		#importiert math-Modul

def volumen (r):		#definiert Funktion "volumen" in Abhängigkeit von r
	V = (r**3)*(4.0/3)*math.pi		#Formel zur Berechnung des Kugelvolumens
	print "Das Volumen einer Kugel mit Radius "+ str(r) + " beträgt "+ str(V)		#gibt Volumen auf den Bildschirm aus
	print "-" * 10		#fügt ein paar Gedankenstriche zur besseren Lesbarkeit des Ergebnisses ein

#Hauptprogramm

r1 = 2.3		#erster Wert für Radius		
volumen(r1)

r2 = 3.9		#zweiter Wert für Radius
volumen(r2)

r3 = 7		#letzter Wert für Radius
volumen(r3)
