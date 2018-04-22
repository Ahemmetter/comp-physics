#-*- coding: utf-8 -*-

"""Testet, ob ein Dreieck mit Seitenlängen a,b und c rechtwinklig ist oder nicht
"""

def Dreieck(a,b,c):		#definiert Funktion Dreieck mit Parametern a,b und c
	
	if type(a) == int and type(b) == int and type(c) == int:
		if a**2 + b**2 == c**2:		#prüft erste Kombination
			print "rechtwinklig"
		elif b**2 + c**2 == a**2:	#prüft zweite Kombination
			print "rechtwinklig"
		elif c**2 + a**2 == b**2:	#prüft dritte Kombination
			print "rechtwinklig"
		else:						#fängt alle "schiefen" Dreiecke ab
			print "schief"
	else:
		print "Bitte geben Sie Zahlen ein."

Dreieck(3,4,5)		#sollte rechtwinklig sein mit a=3, b=4, c=5

Dreieck(2,4,1)

Dreieck(4,53,42)

Dreieck(42, 26, 94)

Dreieck(4,5,3)		#rechtwinklig mit a=4, b=5, c=3

Dreieck(5,3,4)		#rechtwinklig mit a=5, b=3, c=4

Dreieck("hey", "lalala", 3)
