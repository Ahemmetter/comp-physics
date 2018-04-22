#-*- coding: utf-8 -*-
"""Berechnet den Logarithmus zu einer Zahl bei gegebener Basis
"""
import math

def Log(zahl, basis=math.e):
	if type(zahl) == int:
		l = math.log( abs(zahl), basis )
		print l
		print "-" * 10
	else:
		print "Davon kann ich keinen Logarithmus ausrechnen."

Log(2)		#benutzt Standardwert e für Basis

Log(1000,10)

Log(1073741824,2)

Log(2401,7)

Log(-2121, 3)		#als Beispiel für negative Zahl; Python nimmt dann einfach den Betrag der Zahl

Log("apfel", 4)		#als Beispiel für String als Input; Log-Funktion zeigt an, dass das nicht geht
