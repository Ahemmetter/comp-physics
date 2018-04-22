#! /usr/bin/env python

"""Uebung 7: Quantenmechanik von 1D-Potentialen III: Periodische Potentiale

Mit diesem Programm wird die Ausbildung der Bandstruktur fuer ein Periodisches
Potential cos(2 * np.pi * x) abgebildet. Mit einem Mausklick kann im linken
Plotfenster ein k-Wert selektiert werden, fuer den dann das Betragsquadrat
der Eigenfunktionen auf der Hoehe der Eigenenergien im rechten Fenster
ausgegeben werden.
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

def plot_eigenfunktionen(ax, ew, ef, x, V, perioden, width=1, Emax=6, fak=0.25,
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
        title = "Eigenfunktionen"
    plt.axes(ax)                                      # Ortsraumplotfenster
    plt.setp(ax, autoscale_on=False)
    plt.axis([np.min(x), np.max(x), np.min(V), Emax])
    plt.xlabel(r'$x$')
    plt.title(title)

    plt.plot(x, V, linewidth=2, color='k')          # Potential plotten
    anz = np.sum(ew <= Emax)                          # Zahl zu plottenden Ef

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
                # Ef werden periodisch fortgesetzt
                ev = np.abs(np.tile(ef[:, i], perioden))
                plt.plot(x, ew[i] + fak*ev**2, color=colors[i % len(colors)])
    else:                                             # Plot Efkt
        plt.ylabel(r'$V(x)\ \rm{,\ Efkt.\ bei\ EW}$')
        for i in np.arange(anz):
            print ew[i]
            plt.plot(x, ew[i] + fak*ef[:, i], 
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
        # Ausgabe der EF auf Hoehe er EW und als Absolutsbetragsquadrat
        titel="Absolutsbetragsquadrat der Eigenfunktionen"
        plot_eigenfunktionen(eigen, ew, ef, x_per, V_per, perioden,
                betragsquadrat=True, title=titel)
        plt.draw()
        band.lines = band.lines[:-1] # Loeschen der horizontalen Linie
                                           # bei geklicker Bloch-Phase

        
def main():
    # Benutzerfuehrung
    print __doc__
    
    # Einige Variablen muessen fuer die event-Funktion global sein
    global band, eigen, x, x_per, V, V_per, h_eff, perioden
    # zwei Plotbereiche anlegen
    plt.figure(0, figsize = (16, 9))
    band = plt.subplot(121, autoscale_on=False)
    band.set_xlim([-np.pi, np.pi])
    band.set_ylim([-1, 6])
    band.set_title("Bandspektrum 1. Brillouin Zone")
    band.set_ylabel(r"$E$")
    band.set_xlabel(r"$k$")
    
    eigen = plt.subplot(122)
    eigen.set_xlim([0, 4])
    eigen.set_ylim([-1, 6])
    eigen.set_title("Periodisches Potential")
    eigen.set_xlabel(r"$x$")
    eigen.set_ylabel(r"$V(x)$")
    
    
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

    # Erweiterung von x und V auf x (hier 4) Perioden und plot
    x_per = x
    for i in (np.arange(perioden-1)+1):         # i = 0 muss ausgelassen werden
        x_per = np.append(x_per, x + i*(x_max - x_min))
    V_per = np.tile(V, perioden)
    eigen.plot(x_per,V_per, color="k", linewidth=2)


    # Bandspektrum berechnen und bis zu Emax ausgeben
    ew = np.zeros((len(k), len(x)))               # Array fuer EW anlegen
    for i in np.arange(len(k)):                   # EW fuer alle k berechnen
        ew[i, :] = diagonalisierung(h_eff, x, V, k[i])[0]
    energien = ew[:,ew.min(0) <= Emax]            # Nur EW kleiner Emax
    band.plot(k, energien)

    # Ausgabe der Plots und Klick-Abfrage
    plt.connect('button_press_event', plot_k)
    plt.show()


if __name__== "__main__":
    main()
#
#   a) Beobachtungen:
#           k=0: Wie von dem Bandspektrum zu erwarten liegen die Eigenenergien
#               2/3 und 4/5 hier am dichtesten bei einander und man sieht auch,
#               dass die Eigenfunktionen dementsprechend aehnlich aussehen nur
#               gespiegelt, also versch. Symmetrien aufweisen.
#           k=pi: Hier liegen analog zu k=0 die Eigenfunktionen 3/4 und 5/6
#               sehr dicht beieinander. Geht man z.B. mit einem Zoom naeher an
#               die grenze, so kann man sehen wie die Funktionen 5 und 6 stark
#               ihren Wert erhoehen (Welliger werden)
#       Die Variation von k hat auf die Funktionen 1 und 2 fast keine Auswirk-
#       ung. Sie sind durch das Potential gebunden und veraendern sich daher
#       nicht wesentlich. Die anderen Funktionen sind i.a. auch flacher, da das
#       Teilchen hier vom Potential wenig beeinflusst wird und sich daher
#       ueberall gleich wahrscheinlich aufhaelt.
#   b) Verringert man das Potential, so hat das Potential eine deutlich
#       geringere Auswirkung auf die Aufenthaltswahrscheinlichkeit es Teilchens
#       und daher flachen alle Funktionen extem ab. Je nach 'Reststaerke' des
#       Potentials kann man auch noch Welligkeiten also periodisch vom Ort
#       abhaengige Aufenthaltswahrscheinlichkeiten beobachten, dies jedoch nur
#       fuer die ersten beiden bzw. drei Funktionen (bei geschickter Wahl von
#       k) und nur an ausgezeichneten Punkten die bei k=0 und |k|=pi liegen.
