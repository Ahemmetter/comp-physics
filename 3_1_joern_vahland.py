#! /usr/bin/env python

from __future__ import division
import numpy as np
from matplotlib import pyplot as plt


def fkt(x):
    """Auszuwertende Funktion"""
    return np.sin(2*x)

def int_middle(function, x0, x1, n=1000):
    """
    Integration der uebergebenen Funktion 'function' von x0 bis x1
    auf n Teileintervallen. Mittelpunktmethode.
    Rueckgabe: Integalwert, Diskretisierungsbreite dx
    """
    # Array mit linken Intervallgrenzen. n Intervalle
    links = np.linspace(x0, x1, num=n, endpoint=False, retstep=True)
    dx = links[1]                       # Streifenbreite
    werte = function(links[0] + dx/2)   # Fkt-Werte in Intervallmitte
    streifen = dx * werte               # Streifenflaechen
    return (np.sum(streifen), dx)       # Streifen aufsummiert

def int_trapez(function, x0, x1, n=1000):
    """
    Integration der uebergebenen Funktion 'function' von x0 bis x1
    auf n Teilintervallen. Trapezmethode
    Rueckgabe: Integalwert, Diskretisierungsbreite dx
    """
    # Array mit Intervallgrenzen. n Stuetzstellen. rechter Rand inklusive
    stuetz = np.linspace(x0, x1, num=n+1, endpoint=True, retstep=True)
    dx = stuetz[1]                                       # Streifenbreite
    werte = function(stuetz[0])                          # Fkt-Werte an Grenzen
    streifen = (werte[:-1] + werte[1:]) *dx/2            # Streifenflaechen
    return (np.sum(streifen), dx)                        # Streifen aufsummiert

def int_simps(function, x0, x1, n=1000):
    """
    Integration der uebergebenen Funktion 'function' von x0 bis x1
    auf n Teilintervallen. Simpsonmethode
    Rueckgabe: Integalwert, Diskretisierungsbreite dx
    """
    # Array mit Intervallgrenzen 
    stuetz = np.linspace(x0, x1, num=n+1, endpoint=True, retstep=True)
    dx = stuetz [1]                                      # Streifenbreite
    werte = function(stuetz[0])                          # Fkt-Werte an Grenzen
    werte_mitte = function(stuetz[0][:-1] + dx/2)        # Fkt-Werte in Mitte
    streifen = dx/6 * (werte[:-1] + (4 * werte_mitte) + werte[1:])
    return (np.sum(streifen), dx)                        # Streifen aufsummiert

def main():
    """
    Fuerht die numerische Integration der Funktion sin(2*x) mittels der
    Mittelpunkt-, Trapez- und der Simpson-Methode auf dem Intervall
    -pi/2 bis pi/3 durch
    """
    # Integrationsparameter
    function = fkt
    x0       = -np.pi/2
    x1       = np.pi/3
    analytic = -1/4

    # Integration ueber verschiedene Teilintervalle N [1, 10**5]
    N = np.unique(np.int32(np.logspace(0, 5, 1000, endpoint=True)))
    # Array fuer Integralwerte
    val_mid, val_trap, val_sim = np.zeros((3, len(N)))
    # Array fuer Diskretisierungsparameter dx (Teilintervallbreite)
    dx_mid, dx_trap, dx_sim = np.zeros((3, len(N)))
    # Berechnung der Integrale fuer versch. Teilintervalle [1, 10**5]
    for i in np.arange(0, len(N)):
        val_mid[i], dx_mid[i] = int_middle(function, x0, x1, N[i])
        val_trap[i], dx_trap[i] = int_trapez(function, x0, x1, N[i])
        val_sim[i], dx_sim[i] = int_simps(function, x0, x1, N[i])

    # Plot anlegen und konfigurieren
    plt.subplot(111, xscale="log", yscale="log")
    plt.title("Numerische Integration")
    plt.xlabel("dx")
    plt.ylabel(r"$\frac{\Delta I}{I}$ ", fontsize=20)
    # Plot der numerischen Integrale
    plt.plot(dx_mid, np.abs((analytic - val_mid)/analytic),
    label="Mittelpunkt", ls="None", color="r", marker=".", markersize=3)
    plt.plot(dx_trap, np.abs((analytic - val_trap)/analytic),
    label="Trapez", ls="None", color="g", marker=".", markersize=3)
    plt.plot(dx_sim, np.abs((analytic - val_sim)/analytic),
    label="Simpson", ls="None", color="b", marker=".", markersize=3)
    # Plot des zu erwartenden Skalierungsverhalten
    plt.plot(dx_mid, dx_mid**2, label="Skalierung Mittelpunkt & Trapez",
    color="r")
    plt.plot(dx_sim, dx_sim**4, label="Skalierung Simpson", color="b")
    # Plot der Legende und Diagrammausgabe
    plt.legend(loc="upper left")
    plt.show()

if __name__ == "__main__":
    main()


# Analytische Wert der Integrale:
#    a) I = -1/4
#    b) I = sqrt(pi)/10 = 0.1772453850905516
#    c) I = pi/3 = 1.0471975511965976

# Auswertung der numerischen Werte:
#    a) Fuer alle Methoden ergeben sich in doppelt logarithmischer
#       Darstellung Geraden (~ dx**2 bzw. ~dx**4)
#       Fuer die Mittelpunkt und Trapezmethode treten kaum numerische
#       Streuung auf. Die Simpsonmethode verhaelt sich fuer dx in
#       [2*10**(-3), 5/6 * pi] nach der zu erwarteten Skalierung.
#       Fuer kleinere dx dominiert der numerische Fehler --> Rauschen
#
#    b) Die relativen Fehler aller 3 Methoden haben eine aehnliche Form und
#       alle Methoden scheinen etwa gleich genaue Ergebnisse zu liefern:
#       Fuer dx < ~0.05 liegen die Fehler unter 10**-13. Fuer groessere dx
#       nehmen die Fehler drastisch zu, dies liegt dan der Form der Funktion.
#       Die einzigen Werte die einen signifikanten Wert zum Integral beitragen
#       liegen schmal um die y-Achse (x=0). Liegen in diesem interessanten
#       Intervall nur wenige Stuetzstellen wird das Integral entsprechend
#       ungenau.
#
#    c) Fuer alle Methoden entstehen mehrere Geraden, die ungefaehr im Bereich 
#       relativer Fehler von 10**-5 - 1 liegen. Die verschiedenen Geraden
#       haben ihre Uhrsache in der Unstetigkeit bei x=0 und wie die Stuetz-
#       stellen in diesen Bereich fallen.
#       Es faellt ausserdem auf, dass fuer einige wenige dx auch Werte des
#       relativen Fehlers von unter 10**-12 auftreten. Diese sind vermutlich
#       zufaellige Werte bei denen eine Stuetzstelle guenstig auf die
#       Unstetigkeit bei x=0 faellt
