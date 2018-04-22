#! /usr/bin/env python

"""Uebung 8: Ideales Gas - Druckmessung

In diesem Programm wird ein ideales Gas in einem Quader betrachtet. Die
Teilchen stossen an die Seitenwaende und erzeugen so einen Druck. Mit
diesem Programm wird der Druck der auf die rechte Flaeche ausgeuebt 
wird berechnet. Es werden mehrere Realisierungen betrachtet und die
statistische Verteilung betrachtet.
"""

from __future__ import division
from __future__ import print_function
import numpy as np
from numpy import random as random
from matplotlib import pyplot as plt
from matplotlib import mlab as mlab

def reflektionen(x0, v, dt):
    """
    Betrachtet man folgendes einheitenloses Problem. Ein Teilchen 
    befindet sich in einem Quader [0,1] und bewegt sich mit der 
    Geschwindigkeit v. Betrachtet man die Bewegung ueber ein 
    Zeitintervall dt, so wird das Teilchen n mal an der rechten Wand
    (Intervallgrenze) reflektiert. Da die Teilchen sowohl negative oder
    positive Anfangsgeschwindigkeiten haben kann wird der Quader wie
    unten erweitert:
    
    |   :   |   :   |   :   |   :   |   :   |   :   |   :   |
    |   :   |   :   |   :   |   :   |   :   |   :   |   :   |
    |   :   |   :   |   :   |   :   |   :   |   :   |   :   |
    ---------------------------------------------------------
    -7  -6  -5  -4  -3  -2  -1  0   1   2   3   4   5   6   7
    
    Hierbei kann die lineare Translation in Bewegungsrichtung der 
    Anfangsbewegung betrachtet werden und die Reflektionen an der 
    rechten Seite des Quaders koennen an der Fortsetzung betrachtet 
    werden. ein '|' symbolisiert eine reflektion an der rechten Seite
    ein ':' an der linken.
    """
    # Zuerst wird die gesamt Translation bestimmt.
    x = x0 + v * dt
    # Die Anzahl der Reflektionen koennen mit folgender Vorschrift 
    # ermittelt werden. Die Konvertierung in int 32schneidet den 
    # Nachkommateil ab. (Bei x= 2,9 wird nur 1x reflektiert)
    reflektionen = np.int32((np.abs(x) + 1)/ 2)
    return reflektionen
    
def druck(x0, v, dt):
    """Diese Funktion berechnet den einheitenlosen Druck auf die rechte
    Seite eines Quaders.
    Uebergebene Parameter:
        x0 - Anfangsorte der Teilchen
        v  - Anfangsgeschw. der Teilchen
        dt - Zu betrachtendes Zeitintervall
    Ruckgabe:
        p - Von den Teilchen ausgeuebter Druck auf rechte Seite
    """
    N = len(x0)                 # Anzahl der Teilchen   
    # Reflektionen fuer jedes Teilchen bestimmen
    n = reflektionen(x0, v, dt)         
    p_A = 2/(N * dt) * np.dot(np.abs(v), n)
    return p_A
    
def main():
    N = 6
    R = 10000
    dt = 5
    # Druecke fuer R Realisierungen bestimmen
    druecke = np.zeros(R)
    for i in np.arange(R):
        x0 = random.uniform(0, 1, N)
        v  = random.randn(N)
        druecke[i] = druck(x0, v, dt)
    # Mittelwert und Standardabweichung der R Realisierungen bestimmen  
    mittel = np.mean(druecke)
    std = np.std(druecke, ddof=1)
    
    # Konsolenausgabe der Problem Parameter und Benutzerfuehrung
    print(__doc__)
    print("Teilchenzahl: ", N)
    print("Realisierungen: ", R)
    print("Zeitintervall :", dt)
    print("Mittelwert: ", mittel)
    print("Standardabweichung: ", std)
    # Plot anlegen 
    plt.figure(0)
    plt.title("Druckwahrscheinlichkeit")
    plt.xlabel("Druck p")
    plt.ylabel("Wahrscheinlichkeit")
    # Plotten des Histograms fuer 20 Bins und Normierung
    # empfohlene Binanzahl wurde nachgeschlagen bei Wikipedia
    plt.hist(druecke, bins = 20, normed = True)
    # Normalverteilung plotten
    sortiert = np.sort(druecke)
    plt.plot(sortiert, mlab.normpdf(sortiert, mittel, std))
    plt.show()
    
if __name__ == "__main__":
    main()
    
    
# a) N=6:  Der Mittelwert betraegt etwas unter 1 mit einer
#          Standardabweichung von ca. 0.58. Es wird also das nach dem
#          Gasgesetz zu erwartende Wert von p=1.0 abgebildet. Die 
#          Verteilung hat in etwa eine Gausskurve. Sie wird jedoch an
#          linken Seite abgeschnitten. Da die Standardabweichung recht
#          gross ist, der Druck aber stets groesser 0 ist werden nach 
#          rechts mehr Werte angenommen als nach links.
#    N=60: Der Mittelwert liegt jetzt tendenziell eher etwas ueber 1 
#          aber noch sehr nah an 1 (Abweichungen ca. 0.001). Die 
#          Standardabweichung ist mit ca. 0.18 deutlich kleiner geworden
#          weshalb die Gausskurve jetzt deutlich schmaler ist und voll-
#          staendig abgebildet werden kann. 
#
#          Man kann also sehen das beide Parameter den zu erwartenden
#          Wert von 1 abbilden, bei 60 Teilchen die zufaelligen Anfangs-
#          werte jedoch deutlich weniger ins gewicht fallen, was zu 
#          einer schmaleren Gausskurve fuehrt.
# b) 
#          Man erwarted fuer N=6*10**23 Teilchen einen sehr schmalen
#          Peak bei p=1. Dieses Ergebnis bestaetigt den theoretisch
#          zu erwartenden Diskreten Wert, also eine Standardabweichung
#          von 0. Diese Tendenz kann man bereits bei dem Uebergang von 
#          6 zu 60 Teilchen beobachten.

