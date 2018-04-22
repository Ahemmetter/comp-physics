#-*- coding: utf-8 -*-

u"""Durch Anwendung der Mittelpunkt-, Trapez- und Simpsonregeln wird das
bestimmte Integral einer gegebenen Funktion berechnet.
Integrationsgrenzen a und b werden als Parameter übergeben, während die
Anzahl der Stützstellen von 1 bis 100 000 durchiteriert wird. Damit
lässt sich das Skalierungsverhalten der Beträge der relativen Fehler
dieser numerischen Methoden an verschiedenen Funktionen begutachten."""

import numpy as np
from matplotlib import pyplot as plt

def f1(x):
    """Funktion, von der das Integral berechnet werden soll."""
    return np.sin(2*x)

def f2(x):
    """Gaußfunktion"""
    return np.exp(-100*(x**2))

def f3(x):
    """Heaviside-Theta-Funktion"""
    return 0.5 * (1.0+np.sign(x))

def integral(steps, N_array, a, b, f):
    """Berechnet das bestimmte Integral der Funktion f von a nach b
    und benutzt Werte aus N_array als Stützstellenanzahl. Zur Berechnung
    werden Mittelpunktsregel, Trapezregel und Simpsonregel verwendet.
    steps bestimmt die Größe der Arrays."""
    
    mitt = np.zeros(steps)                      # Arrays für die
    trapz = np.zeros(steps)                     # Integrale
    simps = np.zeros(steps)
    
    for i in range(0, steps):
        # Iteration läuft über die verschiedenen Stützpunktanzahlen. Für
        # jedes i wird die x-Achse in dementsprechend viele Teilinter-
        # valle aufgeteilt und das Integral damit angenähert.
        x = np.linspace(a,b,N_array[i], endpoint=False)
        h = (b-a)/N_array[i]
        
        mitt_array = f((2*x+h)/2.0)             # Mittelpunktsregel
        mitt[i] = h * np.sum(mitt_array)
        
        trapz_array = ((f(x+h))+(f(x)))/2.0     # Trapezregel
        trapz[i] = h * np.sum(trapz_array)
        
        simps_array = (1/6.0)*((f(x))+4.0*(f((2*x+h)/2.0))+f(x+h))
        simps[i] = h * np.sum(simps_array)      # Simpsonregel
        
    return mitt, trapz, simps

def rel_Fehler(steps, mitt, trapz, simps, exakt):
    """Berechnet die relativen Fehler der 3 numerischen Methoden.
    Übernimmt die Größe der Arrays, und die Arrays selbst, zusammen
    mit dem analytischen Ergebnis (exakt)."""
    
    mitt_err = np.zeros(steps)                  # Definiert Arrays
    trapz_err = np.zeros(steps)                 # für die relativen
    simps_err = np.zeros(steps)                 # Fehler
    
    mitt_err = abs((mitt - exakt)/exakt)        # berechnet relative
    trapz_err = abs((trapz - exakt)/exakt)      # Fehler
    simps_err = abs((simps - exakt)/exakt)
    
    return mitt_err, trapz_err, simps_err

def main():
    """Definiert die verwendeten Konstanten und plottet die Beträge
    der relativen Fehler, zusammen mit ihrem Skalierungsverhalten."""
    
    print __file__
    print __doc__
    steps = 200                                 # Anzahl der gewählten
                                                # Stützpunktanzahlen
    N_array = np.int32(np.logspace(0.0, 5.0, steps, endpoint=True))
                                                # Stützpunkte, auf log.
                                                # Skala verteilt
    a = -np.pi/2                                # obere Grenze
    b = np.pi/3                                 # untere Grenze
    exakt = -0.25                               # analytisches Ergebnis
                                                # für f1(x)
    mitt, trapz, simps = integral(steps, N_array, a, b, f1)
                                                # Integrale
    
    mitt_err, trapz_err, simps_err = rel_Fehler(steps, mitt, trapz, 
        simps, exakt)                           # Beträge der Fehler
    
    # Plotbefehle:
    fig, ax = plt.subplots(figsize=(14,8))
    ax.plot(((b-a)/N_array), mitt_err, "#588C73", label="Mittelpunkt",
        linestyle="none", marker=".", markersize=4)
    ax.plot(((b-a)/N_array), trapz_err, "#F2AE72",label="Trapez",
        linestyle="none", marker=".", markersize=4)
    ax.plot(((b-a)/N_array), simps_err, "#8C4646", label="Simpson",
        linestyle="none", marker=".", markersize=4)
    ax.plot(((b-a)/N_array), 0.23*((b-a)/N_array)**2, "#588C73")
    ax.plot(((b-a)/N_array), 0.01*((b-a)/N_array)**4, "#8C4646")
    ax.plot(((b-a)/N_array), (b-a)*((b-a)/N_array)**2, "#F2AE72")
    ax.set_yscale("log")                        # doppeltlog. Skala
    ax.set_xscale("log")
    plt.title(u"Beträge der relativen Fehler von 3 numerischen"
        r" Integrationsmethoden am Beispiel von $\sin (2x)$")
    plt.xlabel("Schrittweite $h$")
    plt.ylabel("Betrag des relativen Fehlers")
    ax.legend(loc = "best")                     # Legende
    plt.axis([(b-a)/(10**5.0), 1.0, 10**(-16), 10.0])
    ax.grid()
    plt.show()

if __name__ == "__main__":
    main()

# Analytische Ergebnisse: 
# int_a^b f1(x) dx = -0.25
# int_a^b f2(x) dx =  sqrt(pi)/10
# int_a^b f3(x) dx =  pi/3

# f1: die Fehler von Mittelpunkts- und Trapezregel verhalten sich prop. 
# zu h^2, während die Simpsonregel prop. h^4 verläuft. Bei Mitt. und 
# Trapez. befindet sich der Betrag des Fehlers nicht in der Größen-
# ordnung des Diskretisierungsfehlers. Bei der Simpsonregel allerdings
# bewegt sich der relative Fehler schon für Schrittweiten von ca 10^(-3)
# im Bereich dieses Diskretisierungsfehlers und weicht damit vom vor-
# hergesagten Verlauf ab.

# f2: Alle numerischen Methoden weichen vom vorhergesagten Verlauf ab,
# und zeigen das gleiche Verhalten: im Bereich kleiner Schrittweiten
# unter h = 0.1 liefern alle Methoden den gleichen relativen Fehler,
# darüber ergibt sich eine Streuung von Werten, wobei sich ein
# wachsender Trend erkennen lässt.

# f3: Hier weicht der Fehler der numerischen Methoden wieder vom vor-
# hergesagten Verhalten ~ h^2 bzw ~ h^4 ab. Stattdessen zeigt sich ein
# Verlauf prop. zu h^1 für alle drei Methoden, steigt also langsamer als
# erwartet. Dies liegt daran, dass die betrachtete Funktion an der
# Stelle x = 0 nicht differenzierbar ist und somit keine Taylor-
# entwicklung vorgenommen werden kann. Zu beachten ist, dass sich pro
# Methode mehrere Linien zeigen (4 für Simpsonregel, 3 für Trapez- und
# 2 für Mittelpunktsregel).
