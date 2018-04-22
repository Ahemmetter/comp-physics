#! /usr/bin/env python

"""
"""

from __future__ import division
import numpy as np
from scipy.linalg import eigh
from matplotlib import pyplot as plt

def diskretisierung(xmin, xmax, N):
    """Berechne die quantenmechanisch korrekte Ortsdiskretisierung.

    Parameter:
        xmin: unteres Ende des Bereiches
        xmax: oberes Ende des Bereiches
        N: Anzahl der Diskretisierungspunkte
    Rueckgabe:
        x: Array mit diskretisierten Ortspunkten
    """
    x = np.linspace(xmin, xmax, N, endpoint=False)     # Ortsgitterpunkte
    return x

def potential(x):
    """Gibt das zu betrachtende Potential an den Stellen x zurueck.
    """
    return np.cos(2 * np.pi * x)

def diagonalisierung(hquer, x, V, k):
    """Berechne sortierte Eigenwerte und zugehoerige Eigenfunktionen.

    Parameter:
        hquer: effektives hquer
        x: Ortspunkte
        V: Potentialwerte an x
        k: Bloch-Phase
    Rueckgabe:
        ew: sortierte Eigenwerte (Array der Laenge N)
        ef: entsprechende Eigenvektoren, ef[:, i] (Groesse N*N)
    """
    delta_x = x[1] - x[0]
    N = len(x)
    z = hquer**2/(2.0*delta_x**2)                          # Nebendiagonalelem.
    h = np.array((np.diag(V + 2.0*z) +
         np.diag(-z*np.ones(N - 1), -1) +                  # Hamilton Operator
         np.diag(-z*np.ones(N - 1), 1)),                   
         dtype=complex)
    h[0, N-1] = -z * np.exp(-1j*k)                           # Elemente fuer
    h[N-1, 0] = -z * np.exp( 1j*k)                           # Periodizitaet
    ew, ef = eigh(h)
    ef = ef/np.sqrt(delta_x)
    return ew, ef

def plot_eigenfunktionen(ax, ew, ef, x, V, width=1, Emax=6, fak=0.01,
                         betragsquadrat=False, basislinie=True, alpha=1,
                         title=None):
    """Darstellung der Eigenfunktionen.

    Dargestellt werden die niedrigsten Eigenfunktionen 'ef' im Potential 'V(x)'
    auf Hoehe der Eigenwerte 'ew' in den Plotbereich 'ax'.

    Optionale Parameter:
        width: (mit Default-Wert 1) gibt die Linienstaerke beim Plot der
            Eigenfunktionen an. width kann auch ein Array von Linienstaerken
            sein mit einem spezifischen Wert fuer jede Eigenfunktion.
        Emax: (mit Default-Wert 1/10) legt die Energieobergrenze
            fuer den Plot fest.
        fak: ist ein Skalierungsfaktor fuer die graphische Darstellung
            der Eigenfunktionen.
        betragsquadrat: gibt an, ob das Betragsquadrat der Eigenfunktion oder
            die (reelle!) Eigenfunktion selbst dargestellt wird.
        basislinie: gibt an, ob auf Hoehe der jeweiligen Eigenenergie eine
            gestrichelte graue Linie gezeichnet wird.
        alpha: gibt die Transparenz beim Plot der Eigenfunktionen an (siehe
            auch Matplotlib Dokumentation von plot()). alpha kann auch ein
            Array von Transparenzwerten sein mit einem spezifischen Wert
            fuer jede Eigenfunktion.
        title: Titel fuer den Plot.
    """
    if title is None:
        title = "Asymm. Doppelmuldenpotential"
    plt.axes(ax)                                      # Ortsraumplotfenster
    plt.setp(ax, autoscale_on=False)
    plt.axis([np.min(x), np.max(x), np.min(V), Emax])
    plt.xlabel(r'$x$')
    plt.title(title)

    plt.plot(x, V, linewidth=2, color='0.7')          # Potential plotten
    anz = np.sum(ew <= Emax)                          # Zahl zu plottenden Ef
    print anz
    print ew
    if basislinie:                                    # Plot Basislinie bei Ew
        for i in np.arange(anz):
            plt.plot(x, ew[i] + np.zeros(len(x)), ls='--', color='0.7')

    try:                                              # Verhaelt sich width
        iter(width)                                   # wie ein array?
    except TypeError:                                 # Falls `width` skalar:
        width = width * np.ones(anz)                  # konst. Linienstaerke

    try:                                              # entsprechend fuer
        iter(alpha)                                   # Transparenz alpha
    except TypeError:
        alpha = alpha * np.ones(anz)

    colors = ['b', 'g', 'r', 'c', 'm', 'y']           # feste Farbreihenfolge
    if betragsquadrat:                                # Plot Betragsquadr. Efkt
        plt.ylabel(r'$V(x)\ \rm{,\ \|Efkt.\|^{2}\ bei\ EW}$')
        for i in np.arange(anz):
            plt.plot(x, ew[i] + fak*np.abs(ef[:, i])**2, linewidth=width[i],
                     color=colors[i % len(colors)], alpha=alpha[i])
    else:                                             # Plot Efkt
        plt.ylabel(r'$V(x)\ \rm{,\ Efkt.\ bei\ EW}$')
        for i in np.arange(anz):
            plt.plot(x, ew[i] + fak*ef[:, i], linewidth=width[i],
                     color=colors[i % len(colors)], alpha=alpha[i])

def plot_k(event):
    # Pruefen ob richtiger Plotbereich geklickt
    if plt.get_current_fig_manager().toolbar.mode == '' and event.button == 1\
    and event.inaxes == band:
        eigen.lines = []                                    # Plot aufraeumen
        eigen.plot(x_per, V_per, color="k", linewidth=2)    # Potential plotten
        # geklickte Bloch-Phase mit senkrechter Linie makieren
        band.axvline(event.xdata, c="k")
        # EW und EF fuer geklicktes k berechnen
        ew, ef = diagonalisierung(h_eff, x, V, event.xdata)
        # EF muss periodisch fortgesetzt werden
        ef_per = ef
        for i in np.arange(perioden-1):          # V perioden mal angaengen
            ef_per = np.append(ef_per, ef)
            i += 1
        # Ausgabe der EF auf Hoehe er EW und als Absolutsbetragsquadrat
        plot_eigenfunktionen(eigen, ew, ef, x, V,
                betragsquadrat=True, title="Absolutsbetragsquadrat der EF")


        
def main():
    # Einige Variablen muessen fuer die event-Funktion global sein
    global band, eigen, x, x_per, V, V_per, h_eff, perioden
    # zwei Plotbereiche anlegen
    plt.figure(0, figsize = (16, 9))
    band = plt.subplot(121, autoscale_on=False)
    band.set_xlim([-np.pi, np.pi])
    band.set_ylim([-1, 6])
    band.set_title("Bandspektrum 1. Brillouin Zone")
    band.set_ylabel(r"$E$")
    band.set_xlabel(r"$x$")
    
    eigen = plt.subplot(122)
    eigen.set_xlim([0, 4])
    eigen.set_ylim([-1, 6])
    
    # Variablen und Werte festlegen
    k = np.linspace(-np.pi, np.pi, 100)
    x_min = 0
    x_max = 1
    N_x = 100
    x = diskretisierung(x_min, x_max, N_x)
    V = potential(x)
    h_eff = 0.2
    Emax = 6
    perioden = 4

    # Erweiterung von x und V auf x (hier 4) Perioden
    x_per = x
    for i in (np.arange(perioden-1)+1):          # i = 0 muss ausgelassen werden
        x_per = np.append(x_per, x + i*(x_max - x_min))
    V_per = V
    for i in np.arange(perioden-1):          # V perioden mal angaengen
        V_per = np.append(V_per, V)
        i += 1

    # Bandspektrum berechnen und bis zu Emax ausgeben
    ew = np.zeros((len(k), len(x)))               # Array fuer EW anlegen
    for i in np.arange(len(k)):                   # EW fuer alle k berechnen
        ew[i, :] = diagonalisierung(h_eff, x, V, k[i])[0]
    energien = ew[:,ew.min(0) <= Emax]            # Nur EW kleiner Emax
    band.plot(k, energien)                        # Bandstruktur plotten



    eigen.plot(x_per,V_per, color="k", linewidth=2)

    plt.connect('button_press_event', plot_k)
    plt.show()












if __name__== "__main__":
    main()
