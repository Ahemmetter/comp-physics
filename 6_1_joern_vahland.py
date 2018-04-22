#! /usr/bin/env python

"""Mit diesem Programm wird das Zeitverhalten eines Gaussschen Wellenpaketes in
dem asymmetrischen Doppelmuldenpotential:

        V(x) = x**4 - x**2 + A*x ; A = 0.04

betrachtet. Dem Nutzer wird die Moeglichkeit gegeben in der grafischen Ausgabe
des Potentials mit den eingetragenen Eigenenergien und quadrierten Eigen-
funktionen mittels Linksklick ein neues Gausspaket zu platzieren. Es wird die
Zeitentwicklung und die an der Konstruktion dieser beteiligten Eigenfunktionen
ausgegeben.
"""

from __future__ import division
from __future__ import print_function
import numpy as np
from matplotlib import pyplot as plt
from quantenmechanik import (diskretisierung, diagonalisierung, 
                                plot_eigenfunktionen)

def potential(x, A=0.04):
    """ Rueckgabe des zu betrachtenden Doppelmuldenpotential V(x) mit dem
    Parameter A.
    """
    return x**4 - x**2 + A*x

def wellenpaket(x, x0, p0, h_eff, dx_paket=0.1):
    """Rueckgabe eines Gaussschen Wellenpakets an den orten x mit mittlerem
    Ort x0 und mittlerem Impuls p0 ausserdem koennen die Paketbreite und
    der effektive h-quer wert uebergeben werden
    """
    return(1/((2*np.pi*dx_paket**2)**(1/4)) *
           np.exp((-(x-x0)**2)/(4*dx_paket**2)) *
           np.exp(1j/h_eff * p0 * x))

def zeitentwicklungs_plot(ax, ew, ev, x, V, koeff, h_eff, fak, zeiten):
    """Berechnung der Zeitentwicklung eines Wellenpaketes.

    Uebergebene Variablen:
    ax    - Plottbereich in dem geplottet wird
    ew    - Energieeigenwert
    ev    - Eigenvektor
    x     - Array der Ortsdiskretisierung
    V     - Potential
    koeff - Entwicklungskoeffizienten
    h_eff - Effektives h-quer
    fak   - Skalierungsfaktor der Plotausgabe
    zeiten- Array der Zeiten
    """
    ax.lines = []                                 # Plotfenster aufraeumen
    E0_erwartet = np.dot(np.abs(koeff)**2, ew)    # Energieerwartung
    phi_start = np.dot(ev, koeff)                 # Ausgangswellenpaket
    # Energieerwarung ausgeben
    
    print("Energieerwartungswert des Wellenpakets: ", E0_erwartet)
    # Normierte Anregungswahrscheinlichkeiten (Normierung auf Maximum)
    ws_koeff = np.abs(koeff)**2/np.max(np.abs(koeff)**2)

    # skaliertes Startpaket
    phi_start_skaliert = E0_erwartet + fak*np.abs(phi_start)**2  

    # Plot mit Transparenz proportional zur Anregungsstaerke der Eigenfktn
    plot_eigenfunktionen(ax, ew, ev, x, V, width=1.5, fak=fak,
                            betragsquadrat=True, alpha=ws_koeff,
                            title="Zeitentwicklung eines Wellenpakets")
    # Startpaket plotten
    wellenpaket_entwicklung = plt.plot(x, phi_start_skaliert,
                                linewidth=3, c='k')
    plt.draw()
    
    # Zeitentwicklung:
    for t in zeiten[1:]:
        phi = np.dot(ev, koeff*np.exp(-1j*ew*t/h_eff))  # Berechnung von phi(t)
        # plot abs(phi)**2
        plt.setp(wellenpaket_entwicklung[0],
                 ydata=E0_erwartet + fak*np.abs(phi)**2)
        plt.draw()
    # Benutzerfuehrung
    print ("Neues Wellenpaket zum Entwickeln mit Linksklick starten.")
    print()
    print()

def neues_wellenpaket(event):
    """
    """
    # Fenstermodus und Mausklick ueberpruefen
    if (event.button == 1 and event.inaxes and
            plt.get_current_fig_manager().toolbar.mode == ''):
        # Startpaket
        phi_orig = wellenpaket(x, event.xdata, dx_paket=0.1,
                               p0=p0, h_eff=h_eff)
        # Bestimmung der Entwicklungskoeffizienten
        dx_ort = x[1] -x[0]
        koeff = np.dot(np.conjugate(np.transpose(ev)), phi_orig) * dx_ort
        # Berechnen des Entwickelten Pakets
        phi_neu = np.dot(ev, koeff)
        print("Norm des Fehlers fuer das rekonstruierte Wellenpaket: ",
                       np.sqrt(np.sum(np.abs(phi_neu - phi_orig)**2)*dx_paket))
        zeitentwicklungs_plot(ax, ew, ev, x, V, koeff, h_eff, fak, zeiten)

def main():
    print
    # Einige Globale Variablen (noetig da event verwendet)
    global L, N, x, V, h_eff, Emax, fak, p0, dx_paket, zeiten, ew, ev, ax
    
    L          = 1.5                 # Betrachtetes x-Intervall [-L, L]
    N          = 1000                # Anzahl der Ortspunkte
    x = diskretisierung(-L, L, N)    # ...Ortspunkte

    V = potential(x)                 # Zu betrachtendes Potential
                          
    h_eff      = 0.05                # Effektives h-quer
    Emax       = 0.1                 # Maximal betrachtete Eigenenergie
    fak        = 0.01                # Plot-Skalierungsfaktor

    p0         = 0                   # Impuls des Pakets
    dx_paket   = 0.1                 # Breite des Pakets
    
    zeiten = np.linspace(0, 10, 500) # Zeiten fuer Zeitentwicklung

    ew, ev = diagonalisierung(h_eff, x, V)

    # Plotbereich erstellen
    ax = plt.subplot(111, autoscale_on=False)
    # Eigenfunktionen plotten und Diagramm benennen
    plot_eigenfunktionen(ax, ew, ev, x, V, Emax=Emax, fak=fak,
                         betragsquadrat=True)
    plt.setp(ax,
        title="Asymmetrisches Doppelmuldenpotential mit Eigenfunktionen")

    # Benutzerfuehrung
    print(__doc__)

    # Bereitstellung des Mausklicks und Ausgabe der Zeitentwicklung
    plt.connect('button_press_event', neues_wellenpaket)
    plt.show()
    
    
if __name__ == "__main__":
    main()
#
#       a) Minimum(innerhalb einer Mulde):
#               Das Wellenpaket startet in einer Mulde und 'zerlaeuft' nach
#               aussen und laeuft dann wieder zusammen (das Wellenpaket wird
#               an der Potentialgrenze reflektiert). Es ergibt sich ein recht
#               stabiles Wellenpaket (geringes Zerlaufen und nur geringe
#               oszilation der Paketbreite). 
#          Maximum(oberhalb einer Mulde):
#               Das Wellenpaket zerlaeuft gleichmaessig nach rechts und links.
#               Die Pakete werden and den Grenzen reflektiert und laufen wieder
#               zusammen. Liegt man ein wenig neben dem Maximum (~ x=0) so
#               verhaelt sich das Wellenpaket aehnlich zu 'Minimum' da der
#               klass. verbotene Bereich hier jedoch schmaler ist kann man hier
#               auch transmittierte Anteile beobachten, die erst ganz rechts
#               reflektiert werden (Tunneln)
#
#       b) Minimum:
#               Da das Paket einen Startimpuls hat ist seine Erwartungsenergie
#               groesser als unter a) ausserdem behaelt das Paket seine Form
#               nicht mehr so gut und es faellt auch bei geringerer Start-
#               position an zu tunneln.
#          Maximum:
#               Auch dieses Paket hat eine groessere Erwartungsenergie und
#               liegt daher hoeher. Das Paket laeuft von anfang an nach rechts
#               und zerlaeuft daher nicht mehr symmetrisch. Dies folgt in nicht
#               vorhersagbare Formen des Wellenpaketes
#
#       c) Betrachtet man das Paket ueber einen laengeren Zeitraum, so kann man
#               beobachten, wie das Paket von der einen in die andere Mulde
#               wandert. Das Wellenpaket tunnelt also Stueck fuer Stueck in die
#               andere Mulde. Dies dauert sehr lange da die WS zum tunneln sehr
#               klein ist. Anschliessend wandert das Paket dann wieder zurueck.
#               Im gegebenen Zeitintervall kann man folgenden Verlauf
#               beobachten: 1) --> 2) --> 1) --> 2) Das Paket 'wechselt also'
#               3x die Mulde
