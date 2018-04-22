#! /usr/bin/env python

from __future__ import division           # Garantiert Float division
import numpy as np
from matplotlib import pyplot as plt

"""
Dieses Programm bietet die Funktionen der numerischen Vorwaerts-,
Zentral-, sowie der Extrapolierten Differenz einer Funktion mit quadratischem
Argument im Punkt x mit variablen Parameter h
"""

def forward_difference(function, x, h):
    """
    Diese Funktion uebernimmt eine Funktion als Parameter function und
    berechnet an der Stelle x die Ableitung mittels der Vorwaerts-
    differenz. (Achtung Quadratisches Argument)
    """
    return (1./h * (function((x+h)**2) - function((x)**2)))

def central_difference(function, x, h):
    """
    Diese Funktion uebernimmt eine Funktion als Parameter function und
    berechnet an der Stelle x die Ableitung mittels der Zentral-
    differenz. (Achtung Quadratisches Argument)
    """
    return (1./h * (function((x + h/2)**2) - function((x - h/2)**2)))

def expol_difference(function, x, h):
    """
    Diese Funktion uebernimmt eine Funktion als Parameter function und
    berechnet an der Stelle x die Ableitung mittels der Zentral-
    differenz. (Achtung Quadratisches Argument)
    """
    return (1./(3*h) *(8 * (function((x + h/4)**2) - function((x - h/4)**2)) -
           (function((x + h/2)**2) - function((x - h/2)**2))))

def main():
    # Berechnen der Numerischen Ableitung von np.arctan an der Stelle 
    # x = 1/3 mit den 3 gegebenen Funktionnen mit variablen Parameter h im
    # Intervall [10**(-10), 1]
    h = np.logspace(-10, 0, num=1001, endpoint=True)
    forward = forward_difference(np.arctan, (1/3), h)
    central = central_difference(np.arctan, (1/3), h)
    expol   = expol_difference(np.arctan, (1/3), h)
    # Analytisch ermittelter Wert
    truevalue = 27./41
    # Berechnung des Relativen Fehlers
    error_forward = np.abs((forward - truevalue) / truevalue)
    error_central = np.abs((central - truevalue) / truevalue)
    error_expol   = np.abs((expol - truevalue) / truevalue)


    # Minima herausfinden und per Konsole ausgeben (Array minimum Index
    # suchen und Werte aus h bzw. error Arrays aufrufen)
    forward_min = (np.argmin(error_forward))
    print ("Forward min: h = " + str(h[forward_min]) + "       error = " +
    str(error_forward[forward_min]))
    central_min = (np.argmin(error_central))
    print ("central min: h = " + str(h[central_min]) + "       error = " +
    str(error_central[central_min]))
    expol_min = (np.argmin(error_expol))
    print ("Exrapoliert min: h = " + str(h[expol_min]) + "       error = " +
    str(error_expol[expol_min]))


    # Grafikfenster einrichten
    plt.figure(0, figsize=(18, 10))
    plt.subplot(111, xscale="log", yscale="log")
    plt.title("Numerische Ableitungen")
    # Numerische Ableitungen fuer verschiedene Werte h plotten
    plt.plot(h, error_forward, label="Vorwaertsdifferenz", ls="None",
    marker=".", color="r")
    plt.plot(h, error_central, label="Zentraldifferenz", ls="None",
    marker=".", color="g")
    plt.plot(h, error_expol, label="Extrapoliertedifferenz",
    ls=".", marker=".", color="b")
    # Skalierungsverhalten plotten
    plt.plot(h, h,    color="r", label="Skalierung $h$")
    plt.plot(h, h**2, color="g", label="Skalierung $h^2$")
    plt.plot(h, h**4, color="b", label="Skalierung $h^4$")
    # Achsenkonfiguration und Legende
    plt.xlabel("h")
    plt.ylabel("relativer Fehler")
    plt.ylim(10**(-16), 1)
    plt.legend(loc="upper left")
    plt.show()
    
if __name__=="__main__":
    main()


# In den bei der Bestimmung der nummerischen Ableitung treten verschiedene
# Fehlertypen auf:
#    1.) zum einen ist der Alorithmus an sich fehlerbehaftet. Die Vorwaerts-
#    methode ist in sich Ungenauer als zum Beispiel die Zentralmethode.
#    2.) ausserdem treten bei dem Bilden der Differenz Rundungsfehler auf,
#    diese Fehler sind jedoch Python intern und koennen nicht durch
#    alternative Algorithmen ausgemerzt werden.
#
# Der minimale Fehler wird also erreicht wenn die Summe aus den Fehlern 1)
# und 2) minimal ist.
#
# Die Minimalen Fehler mit zugehoerigem h werdem per Konsole ausgegeben.
# waehlt man bei der Array-Laenge num=1000 liefert die Extrapolierte
# Differenz einen Error von 0. Vermutlich ein interner Rundungsfehler...
# Daher wurde num=1001 gewaehlt.
