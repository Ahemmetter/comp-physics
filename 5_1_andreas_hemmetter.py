#-*- coding: utf-8 -*-

u"""Dieses Programm bestimmt die Eigenwerte und Eigenfunktionen zum
gegebenen Potential numerisch und plottet diese um ihren Eigenwert
versetzt im Potential. Zur Überprüfung der Ergebnisse kann der
harmonische Oszillator betrachtet werden, dessen Energieeigenwerte durch
E_n = hbar omega (1/2 + n) gegeben sind.

Verwendete Parameter:
A: Asymmetrieparameter
hbar: effektiver Diskretisierungsparameter
xmin, xmax: Grenzen
N: Stützstellen
E_max: maximales Energieniveau
k: Skalierungsfaktor
"""

import numpy as np                                  # Importbefehle
from matplotlib import pyplot as plt
from scipy.linalg import eigh

def V_harm(x, A):
    u"""Potential des harmonischen Oszillators, Parameter A wird nur
    übergeben, damit die Funktion später so aufgerufen werden kann,
    wie die des Doppelmuldenpotentials."""
    return 0.5*x**2

def V_doppel(x, A):
    """Doppelmuldenpotential mit A als Asymmetrieparameter"""
    return x**4 - x**2 - A*x

def eigen(V, N, A, e_max, hbar, xmax, xmin):
    u"""Bestimmt Eigenfunktionen und Eigenwerte zum gegebenen Hamilton-
    ian mittels der scipy-Funktion eigh(). Der Diskretisierungsparameter
    wurde aus der Anzahl der Stützstellen N berechnet."""
    
    dx = abs(xmax - xmin) / N                       # Schrittweite
    i = np.arange(0, N)                             # Integer-Hilfsarray
    z = (hbar**2) / (2 * (dx ** 2))                 # Diskretisierungsp.
    
    V_array = V(xmin + i * dx, A)                   # Potentialarray
    
    H = (np.diag(V_array + (2*z)) + np.diag(np.ones(N-1) * -z, -1)
        + np.diag(np.ones(N-1) * -z, 1))            # Hamiltonian
    
    ew, ef = eigh(H)                                # Eigenfunkt. und
                                                    # -werte
    e_aus = (ew <= e_max)                           # EW werden bis zu
                                                    # E_max ausgewählt
    ew = ew[e_aus]
    ef = ef[:, e_aus]/(dx ** 0.5)                   # EF werden bis zu
                                                    # E_max ausgewählt
                                                    # und normiert
    return ew, ef

def eigen_plot(ew, ef, N, xmax, xmin, k):
    """Plottet Eigenfunktionen und Eigenwerte in den Potentialplot"""
    
    x = np.linspace(xmin, xmax, N)                  # x-Achseneinteilung
    
    for i in range(len(ew)):
        # plottet EF um ihren EW verschoben in rot, höhere Energie-
        # niveaus werden dünner gezeichnet. EW werden als gestrichelte
        # Linien eingezeichnet.
        plt.plot(x, ew[i] + k * ef[:, i], color="#D91E18", 
            linewidth = abs(len(ew)-i)*0.15+0.4)
        plt.text(xmin+0.1, ew[i]+0.005, str(r"$%.3f$" % ew[i]))
        plt.plot(x, ew[i]*np.ones(N), color="#6C7A89", linestyle = "--")
    plt.draw()

def pot_plot(V, x, A, fig):
    """Plottet das ausgesuchte Potential"""
    fig.plot(x, V(x, A), color= "k", linewidth = 1)
    plt.draw()

def select_pot(V, x, A, N, e_max, hbar, xmax, xmin, fig, k, potentials):
    """Skaliert den Plotbereich und passt ihn an das gewählte Potential
    an. Durch das verwendete dictionary kann auch die Funktion des
    Potentials im Titel ausgegeben werden."""
    ymin = np.amin(V(x, A))*1.1                     # Untergrenze des
    # Plots wird entsprechend des kleinsten Wertes im Potential gewählt
    # und mit 10% padding versehen.
    ew, ef = eigen(V, N, A, e_max, hbar, xmax, xmin)
    # Plottet EF, EW und Potential
    pot_plot(V, x, A, fig)
    plt.title("Eigenwerte und Eigenfunktionen von " + r"$V = $ " + 
        potentials[V.__name__])                     # Ausgabe des Titels
    eigen_plot(ew, ef, N, xmax, xmin, k)
    return ymin

def main():
    """Definiert Parameter und zeigt Benutzerführung an."""
    N = 100                                         # Stützstellen
    A = 0.05                                        # Asymmetrieparam.
    e_max = 0.15                                    # Maximale Energie
    hbar = 0.07                                     # effektives h_bar
    xmax = 1.5                                      # Obergrenze
    xmin = -1.5                                     # Untergrenze
    k = 0.015                                       # Skalierungsfaktor
    potentials = {"V_harm" : r"$\frac{1}{2}x^2$",   # dictionary für
        "V_doppel":r"$x^4 - x^2 - Ax$"}             # Potentialfunkt.
    x = np.linspace(xmin, xmax, N)                  # x-Achseneinteilung
    ymax = e_max*1.25                               # y-Obergrenze mit
                                                    # 25% padding
    
    print __file__                                  # Benutzerführung
    print __doc__
    
    plt.figure (0, figsize= (10, 12))               # Plotfenster
    fig = plt.subplot(111)
    
    plt.xlabel("$x$")                               # Beschriftung
    plt.ylabel("$E$")
    ymin = select_pot(V_doppel, x, A, N, e_max, hbar, xmax, xmin, fig, 
        k, potentials)                              # Plotbefehle
    plt.axis([xmin, xmax, ymin, ymax])
    
    fig.plot(x, 0.0*x+e_max, color = "b", linewidth = 1)
                                                    # Plotbefehl für
                                                    # E_max
    fig.text(xmin+0.1, e_max+0.005, r"$E_{max} = $ " + 
        str(r"$ %.3f$" % e_max))                    # Beschriftungen
                                                    # der EW
    plt.show()

if __name__ == "__main__":
    main()

# a.    Die Intervallgröße wurde so gewählt, dass der gesamte Potential-
#       bereich im interessanten Energiebereich (bis E_max) sichtbar
#       bleibt (mit Platz am Rand). Die Eigenfunktionen fallen an der
#       Potentialgrenze exponentiell ab und sind im Bereich -1,5 bis 1,5
#       praktisch bereits auf 0 abgefallen.
#       Die Matrixgröße wurde so gewählt, dass die charakteristische
#       Form der Eigenfunktionen erkennbar bleibt, aber nicht zu groß,
#       um den Rechenaufwand so gering wie möglich zu halten. (N = 100)
#       Diese Wahl liefert einen glatten Funktionsverlauf.
# b.    Der Knotensatz lässt sich am harmonischen Potential besonders
#       einfach erkennen, hier entspricht die Anzahl der Knoten jeweils
#       dem um 1 verminderten Wert des Energieniveaus: k = n-1. So hat
#       zB der Grundzustand mit n=1: k = n-1 = 0 Knoten. Ein kleineres
#       h_eff (hbar) vergrößert die Anzahl der Eigenwerte unterhalb von
#       E_max und verkleinert den Energieabstand zwischen geraden und
#       ungeraden Zuständen.
# c.    Im Falle von A=0 scheinen die ersten 4 Zustände entartet zu sein
#       (Grundzustand und erstes Niveau sind entartet und 3. und 4. 
#       Zustand). Das Potential ist symmetrisch.
