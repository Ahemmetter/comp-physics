#-*- coding: utf-8 -*-

"""Testet, ob ein bestimmter Exponent eine Mersenne-Primzahl ergibt."""

def MersennePrimzahl(p):
	"""Funktion MersennePrimzahl übernimmt Parameter p 
	(Exponent von 2**p-1) und testet, ob das daraus resultierende m 
	eine Primzahl ist oder nicht. Im Grunde wird somit der
	Lucas-Lehmer-Test genutzt."""
	m=2**p-1
	s=4
	for i in range (2,p):
		s = (s*s-2)%m
	if not s==0:
		print 'keine Primzahl'
	else:
		print 'Primzahl'
		print m #Gibt Primzahl im Dezimalsystem aus
		print "{0:#b}".format(m) #Gibt Primzahl im Binärsystem aus 
		#(Für Mersenne-Primzahlen sind das nur Einsen)


#Hauptprogramm mit Versuchswerten
MersennePrimzahl(3)
MersennePrimzahl(42)
MersennePrimzahl(26)
MersennePrimzahl(11213) #Bestimmung dieses Wertes dauert relativ lange
