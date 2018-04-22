#!/usr/bin/python                    #Header

"""Dieses Programm stellt Funktionen zum bilden der Standardabbildung
bereit und gibt die Moeglichkeit im Phasenraum-Diagramm mit Linksklick
die Startbedingungen zu waehlen. 
"""

import numpy as np
import matplotlib.pyplot as plt


def positions(theta_0, p_0, n=1000):
    """
    Dieses Programm bildet die Standardabbildung des gekickten Rotors 
    auf dem Torus und gibt die Werte theta und p als Arrays zurueck.
    """
    t = np.zeros(n);                 # Koordinaten-Array mit Start-
    p = np.zeros(n);                 # werten anlegen
    t[0] = theta_0
    p[0] = p_0 
    
    for i in np.arange(1,n):         # n Werte iterativ bestimmen
        t[i] = ((t[i-1] + p[i-1]) % (2 * np.pi))
        p[i] = ((p[i-1]+K*np.sin(t[i])) + np.pi) % (2*np.pi) - np.pi
    return t, p


def mouse_click(event):
    """Diese Funktion uebernimmt die Koordinaten im Diagramm bei
    Linksklick und plottet von diesen Werten ausgehend 1000 Punkte 
    des gekickten Rotors
    """
    mode = plt.get_current_fig_manager().toolbar.mode
    # Prueft ob Zoom deaktiviert ist und ob mit links geklickt wird
    if event.button == 1 and event.inaxes and mode == '':
        x, y = positions(event.xdata, event.ydata)
        plt.plot(x, y,linestyle="none", marker=".", markersize=1)
        plt.draw()
    

if __name__=="__main__":             # Hauptprogramm
    K=2.6                            # Parameter fuer Standardabbildung
    
        # Benutzerinformationen
    print ("""Waehlen Sie mit Linksklick einen Punkt im Phasenraum"""
    """diagramm aus. Von diesem Punkt aus werden die Koordinaten fuer"""
    """ 1000 Kicks des Rotors berechnet und geplottet.""")
       
    plt.figure(1)                    # Einrichtung des Fensters
    plt.subplot(111)                 # und Einrichtung der Achsen
    plt.title("phase space diagram for kicked rotor")
    plt.axis([0, 2*np.pi, -np.pi, np.pi])
    plt.xlabel(r"$\theta$", fontsize=20)
    plt.ylabel(r"$p_n$" , fontsize=20)
    # Einrichten der Mausinteraktion und Endlosschleife
    plt.connect('button_press_event', mouse_click)
    plt.show()
    

# Beobachtungen:

# Mit steigendem Wert fuer den Parameter K sinken die Bereiche fuer 
# regulaere Zustaende. Zoomt man in regulaere Bereiche hinein sieht man
# ein aehnliches Bild wie in der herausgezoomten Ansicht: Um das Zentrum
# der regulaeren Bereiche sieht man weitere regulaere Inseln.

