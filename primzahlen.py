#-*- coding_ utf-8-*-

"""Berechnung der ersten Primzahlen bis 100
"""

for zahl in range(2, 101):
    ist_primzahl = True     #Schalter, der die Ausgabe triggert
    for i in range(2,zahl):     #Testen, ob Teiler existieren
        if ( (zahl%i == 0) and (zahl>2) ):  #ist Primzahl und muss ausgeschlossen werden
            ist_primzahl = False
    if (ist_primzahl == True):
            print zahl
