#-*- coding: utf-8 -*-

u"""Dieses Programm berechnet die Ableitung der gegebenen Funktion
np.arctan(x**3) an der Stelle x = 1.0/3 auf drei verschiedene numerische 
Arten: vorwärts, zentral und extrapoliert. Die erhaltenen Werte werden 
für verschiedene Stützpunktanzahlen mit dem analytischen Ergebnis 
verglichen und der relative Fehler geplottet. Zum Vergleich wird das 
erwartete Skalierungsverhalten in das gleiche Fenster geplottet, welches
sich aus der Taylorentwicklung der Definition des Differenzenquotienten 
ergibt.
Andreas Hemmetter, 3957650"""

import numpy as np                          # Importbefehle
from matplotlib import pyplot as plt

def f(x):
    """Definition der Testfunktion"""
    y = np.arctan(x**3)
    return y

def derivate(h, x):
    """Berechnet die Ableitung an der Stelle x auf 3 verschiedene
    Arten (vorwärts, zentral und extrapoliert) und analytisch.
    Übernimmt eine Liste mit den verschiedenen Werten für die
    Stützstellen und die Stelle x."""
    
    a = []                                  # Listen für die Ableitungen
    v = []
    z = []
    e = []
    
    for i in h:
        
        abl_a = (3*x**2) / (x**6 + 1)       # analytisch
        a.append(abl_a)
        
        abl_v = (1/i) * (f(x+i) - f(x))     # vorwärtsdifferenziert
        v.append(abl_v)
        
        abl_z = 1/i * (f(x+i/2)- f(x-i/2))  # zentral
        z.append(abl_z)
        
        abl_e = 1/(3*i) * ((8*(f(x+i/4) - f(x-i/4))
            - (f(x+i/2) - f(x-i/2))))       # extrapolierte Diff.
        e.append(abl_e)

    return a, v, z, e

def rel_Fehler(h, v, a, z, e):
    """Berechnet die relativen Fehler der 3 numerischen Methoden.
    Übernimmt die berechneten Ableitungen, sowie die h-Liste."""

    v_err = []                              # Listen für relative Fehler
    z_err = []
    e_err = []
    
    for i in range(0, len(h)):
        # berechnet die relativen Fehler für jeden Stützpunktwert
        v_err.append((abs(v[i] - a[i]))/a[i])
        z_err.append((abs(z[i] - a[i]))/a[i])
        e_err.append((abs(e[i] - a[i]))/a[i])
        
    return v_err, z_err, e_err

def skalierung(h):
    """Berechnet das erwartete Skalierungsverhalten in 
    Abhängigkeit von h."""

    v_h = []                                # Listen für
    z_h = []                                # Skalierungsverhalten
    e_h = []
    
    for i in range(0, len(h)):
        
        # füllt Liste mit erwarteten Werten für das Skalierungsverhalten
        # von h. Die Vorfaktoren wurden mit Wolframalpha berechnet, für
        # den letzten kürzt er sich weg.
        
        v_h.append((529983/266450/2.0)*h[i])
        z_h.append((561212631/97254250/24.0)*h[i]**2)
        e_h.append(10**(-2)*h[i]**4)
        
    return v_h, z_h, e_h

def main():
    """Mainfunktion. Initialisiert das Plotfenster und legt das Aus-
    sehen des Plots fest (Farbe etc.)."""
    
    print __file__
    print __doc__
    
    N = 100
    # logarithmisch verteilte Stützpunkte (N Stück). Bei linearer 
    # Verteilung der Punkte erhält man eine ungünstige Verteilung der
    # Punkte auf einer logarithmischen Skala, welche sich im Bereich
    # von großen Zahlen (~1) häufen
    h = np.logspace(-10.0, 0.0, N)             
    x = 1.0/3                               # Stelle, an der die 
                                            # Ableitung berechnet wird
    # Die Ableitungen werden berechnet, danach die Beträge der Fehler
    # und anschließend das Skalierungsverhalten.
    a, v, z, e = derivate(h, x)
    v_err, z_err, e_err = rel_Fehler(h, v, a, z, e)
    v_h, z_h, e_h = skalierung(h)
    
    fig, ax = plt.subplots(figsize=(14,8))  # Größe des Plotfensters
    ax.plot(h, v_err, "#588C73", label=u"vorwärts")
    ax.plot(h, v_h, "#588C73", linestyle = "dashed", label="~$h^1$")
    ax.plot(h, z_err, "#F2AE72",label="zentral")
    ax.plot(h, z_h, "#F2AE72", linestyle = "dashed", label="~$h^2$")
    ax.plot(h, e_err, "#8C4646", label="extrapoliert")
    ax.plot(h, e_h, "#8C4646", linestyle = "dashed", label="~$h^4$")
    ax.set_xscale("log")                    # logarithmische Skala
    ax.set_yscale("log")
    plt.xlabel("Schrittweite $h$")
    plt.ylabel("Betrag des relativen Fehlers")
    plt.title("Vergleich verschiedener Methoden zur Differentiation "
        r"mit $f(x) = \arctan(x^3)$")
    ax.legend(loc='upper left')             # Legende
    plt.axis([10**(-10), 1.0, 10**(-16), 10.0])
                                            # Fensterausschnitt wird t
    ax.grid()                               # festgeleg Gitternetz zum
                                            # Ablesen von h
    plt.show()

if __name__ == "__main__":
    main()

# Beobachtungen: Der relativ Fehler der Differentiation wird nicht immer
# kleiner, je kürzer man die Abstände der Stützpunkte wählt. Ab einer
# bestimmten Größe vergrößert sich der Fehler wieder, da die Zahlen auf 
# die nächste maschinenlesbare Zahl gerundet oder abgeschnitten werden. 
# Dies führt zu einem immer größeren Rundungsfehler, der sich im Bereich 
# h < 10**(-3) bis 10**(-9) auswirkt.
# Für die Vorwärtsdifferenz ergibt sich das Skalierungsverhalten aus der
# Taylorentwicklung des Differenzenquotienten. Hierbei kürzen sich alle
# Terme bis auf O(h) und einen Vorfaktor weg, was bedeutet, dass sich 
# der Quotient in erster Näherung proportional zu h verhält. Bei den 
# anderen Methoden funktioniert dies analog, allerdings ergeben sich
# hier O(h**2) und O(h**4).

# Optimale Wahl von h:
# Methode      |   h_min
# --------------------------
# vorwärts     | 8*10**(-2)
# zentral      | 6*10**(-5)
# extrapoliert | 5*10**(-8)
