#-*- coding: utf-8 -*-

"""Berechnet die Eigenfunktionen und Eigenenergien eines periodischen
Potentials bei freier Wahl der Blochphase.
Ein Klick in den linken Plotbereich wählt eine neue Phase aus.
"""

import functools
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh


def V(x, A):
    """Potential V(x) = A*cos(2*pi*x) mit Ort x und Amplitude A"""
    return A*np.cos(2*np.pi*x)

def diskretisierung(xmin, xmax, N, retstep=False):
    """Berechne die quantenmechanisch korrekte Ortsdiskretisierung.

    Parameter:
        xmin: unteres Ende des Bereiches
        xmax: oberes Ende des Bereiches
        N: Anzahl der Diskretisierungspunkte
        retstep: entscheidet, ob Schrittweite zurueckgegeben wird
    Rueckgabe:
        x: Array mit diskretisierten Ortspunkten
        delta_x (nur wenn `retstep` True ist): Ortsgitterabstand
    """
    delta_x = (xmax - xmin) / (N + 1.0)     # Ortsgitterabstand
    x = np.linspace(xmin+delta_x, xmax-delta_x, N)  # Ortsgitterpunkte

    if retstep:
        return x, delta_x
    else:
        return x

def diagonalisierung(hbar, x, V, k):
    """Berechne sortierte Eigenwerte und zugehoerige Eigenfunktionen.

    Parameter:
        hquer: effektives hquer
        x: Ortspunkte
        V: Potentialwerte an x
        k: Blochphase
    Rueckgabe:
        ew: sortierte Eigenwerte (Array der Laenge N)
        ef: entsprechende Eigenvektoren, ef[:, i] (Groesse N*N)
    """
    delta_x = x[1]-x[0]
    N = len(x)
    z = hbar**2 / (2.0*delta_x**2)          # Nebendiagonalelem.
    h = np.zeros((N,N), dtype=np.complex)
    h = (np.diag(V + 2.0*z) +               # Hamiltonian
         np.diag(-z*np.ones(N-1), -1) +
         np.diag(-z*np.ones(N-1), 1) + 
         np.diag([-z*np.exp(1j*k)], N-1)  + 
         np.diag([-z*np.exp(-1j*k)], -(N-1)))
    ew, ef = eigh(h)                        # Diagonalisierung
    ef = ef/np.sqrt(delta_x)                # WS-Normierung
    return ew, ef

def plot_eigenfunktionen(x, V, ax2, hbar, k, E_max_n, skal, colors, 
    x_periodisch, perioden, V_periodisch):
    """Plottet die Eigenfunktionen und Eigenwerte in das rechte
    Plotfenster periodisch fortgesetzt."""
    
    ax2.cla()                               # löscht Plotbereich
    ew, ef = diagonalisierung(hbar, x, V, k)
    delta_x = x[1]-x[0]                     # Schrittweite aus x
    
    for l in range(perioden):               # Loop über Perioden
        for i in range(E_max_n):            # Loop über Energien
            # plottet EW
            ax2.plot(x_periodisch, ew[i]*np.ones(len(x_periodisch)), 
                color=colors[i % len(colors)], ls='--')
            # plottet EF, periodisch fortgesetzt
            ax2.plot(x+l, ew[i]*np.ones(len(x)) + 
                skal/np.sqrt(delta_x)*np.abs(ef[:, i])**2, 
                color=colors[i % len(colors)], ls='-')
            ax2.axis([0, 4, -1, 7.5])       # legt Subplotgröße fest
    plt.draw()
                     
def onclick(event, ax1, x, V, ax2, skal, hbar, E_max_n, perioden,
    colors, V_periodisch, x_periodisch, k):
    """Bei einem Klick ins linke Plotfenster werden mit der x-Klick-
    koordinate neue EW und EF geplottet."""
    mode = plt.get_current_fig_manager().toolbar.mode
    if event.button == 1 and event.inaxes == ax1 and mode == '':
    # Abfrage, ob in ax1 geklickt wurde
        k0 = event.xdata                    # Klickkoordinate
        # Anzeige der Klickposition durch Linie
        ax1.axvline(k0, color='k', linestyle='--')
        # Plotfunktion wird mit neuem k-Wert k0 aufgerufen
        plot_eigenfunktionen(x=x, V=V, ax2=ax2, hbar=hbar, k=k0, 
            E_max_n = E_max_n, skal=skal, colors=colors, 
            x_periodisch=x_periodisch, perioden=perioden, 
            V_periodisch=V_periodisch)
        # Periodisches Potential wird gezeichnet
        ax2.plot(x_periodisch, V_periodisch, color='k', linewidth=2)
        plt.draw()

def main():
    """Hauptprogramm"""

    print __file__
    print __doc__

    A = 1                                   # Amplitude
    E_max_n = 6                             # Anzahl an EW
    perioden = 4                            # Anzahl an Perioden    
    hbar = 0.2                              # effektives hbar
    N = 100                                 # Schrittanzahl
    skal = 0.015                            # Skalierungsfaktor
    xmin = 0                                # Intervallgrenzen
    xmax = 1
    
    k = np.linspace(-np.pi, np.pi, N)       # Blochphase
    x = diskretisierung(xmin, xmax, N)      # x-Koordinaten
    pot = V(x, A)                           # Array aus Potential
    colors = ['g', 'b', 'c', 'r', 'y', 'k'] # Farbabfolge
    fig = plt.figure(0, figsize=(14, 10))   # Plotfenster
    ax1 = fig.add_subplot(121)              # Subplots
    ax2=fig.add_subplot(122)
    
    energien = np.zeros((E_max_n, N), dtype=np.float)
    
    for i in range(N):
        # Auswahl der Energien
        ew, ef = diagonalisierung(hbar, x, pot, k[i])
        e_aus = ew[:E_max_n]
        energien[:,i] = e_aus

    for i in range(E_max_n):
        # plottet Energien (Bandstruktur)
        ax1.plot(k, energien[i, :])
    
    x_periodisch = x
    # periodische Fortsetzung des x-Arrays
    for i in (np.arange(perioden-1)+1):
        x_periodisch = np.append(x_periodisch, x + i*(xmax - xmin))
    
    V_periodisch = pot
    # periodische Fortsetzung des Potentials
    for i in np.arange(perioden-1):
        V_periodisch = np.append(V_periodisch, pot)
        i += 1
    
    ax1.set_title(r"$E(k)$")
    ax1.set_xlabel(r"$k$")
    ax1.set_ylabel(r"$E$")
    ax1.axis([k[0], k[-1], 0, np.amax(energien)+0.05])
    
    ax2.set_title("Eigenwerte und Eigenfunktionen")
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$E$, $|\psi(x)|^2$")  
    ax2.axis([0, 4, 0, np.amax(energien)+0.05])

    klick_funktion = functools.partial(onclick, ax1=ax1, x=x,
        V=pot, ax2=ax2, skal=skal, hbar=hbar, E_max_n=E_max_n,
        perioden=perioden, colors=colors, V_periodisch=V_periodisch, 
        x_periodisch=x_periodisch, k=k)
    plt.connect('button_press_event', klick_funktion)
    plt.show()
    
if __name__ == "__main__":
    main()

#       Aufgaben:
#
# a.    Die Bänder sind parabelförmig mit positiver und negativer
#       Steigung. Am Zonenrand findet mal eine Energielücke. Die Bänder
#       sind da aufgespalten. Jede zweite Eigenenergie nimmt mit
#       wachsendem k zu, die anderen ab.
#       k = 0: EF sind ebene Wellen (sin), da die kinetische Energie
#       0 ist. Das 4. und 5. Band sind fast entartet.
#       k = pi: Das 3. und 4. bzw 5. und 6. Band sind fast entartet.
#       Die EF sind cos-förmig. Hier ist die Bragg-Bedingung erfüllt und
#       es bilden sich stehende Wellen.
#
# b.    A << 1: das System entspricht dem der (fast) freien Elektronen.
#       Die Wahrscheinlichkeitsverteilung der Elektronen ist
#       oszillierend und nahezu gleichverteilt.

