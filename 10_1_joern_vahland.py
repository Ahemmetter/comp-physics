#! /usr/bin/env python

"""Uebung 10: Ising-Modell
Mit diesem Programm wird der Spinzustand eines 50x50 Gitters mit periodischen
Randbedingungen dargestellt. Es wird ausserdem die mittlere Magnetisierung der
Spins ueber der dimensionslosen Temperatur tau abgebildet. Im rechten Fenster
kann per Mausklick ein Ausgangszustand (tau und m) gewaehlt werden, welcher
auch im Gitter dargestellt wird. Ein Klick in das linke Fenster startet die
Simulation von 10 Monte-Carlo-Zeitschritten. Es wird die Aenderung der Spin-
Zustaende und der mittleren Magnetisierung dynamisch abgebildet.
"""

from __future__ import division
import numpy as np
from matplotlib import pyplot as plt

def m_inf(t):
    """Diese Funktion stellt die analytischen Werte fuer m_inf fuer die Zeiten
    t bereit.
    """
    # Setzte m=0 da fuer t > t_c eh m=0
    m = np.zeros(len(t))
    t_c = 2 / np.arcsinh(1)
    # Berechne richtige Werte fuer m fuer t < t_c
    m [ t < t_c ] =  (1 - (1 / np.sinh(2/t[ t < t_c ])**4))**(1/8)
    return m


def spinzustand_neu(m, n=50):
    """Diese Funktion berechnet zufaellige Spins fuer ein n x n Gitter mit den
    Spin-Werten -1 und 1. Es kann die mittlere Magnetisierung m pro Spin uber-
    geben werden.
    """
    N = n**2              # Anzahl der Gitterpunkte
    # Wahrscheinlichkeiten fuer Magn. +/- kann leicht aus p(-) + p(+) = 1 und
    # <m> = 1/N sum(p_i(+) - p_i(-) bestimmt werden
    p_plus = (m + 1)/2    
    p_minus = 1 - p_plus  
    spins = [-1, 1]       # Spinmoeglichkeiten
    # Bestimme Spins fuer n x n Gitter mit entspr. Wahrscheinlichkeit
    gitter = np.random.choice(spins, size=(n, n), p=[p_minus, p_plus])
    return gitter

def monte_carlo(gitter, n=50):
    """Diese Funktion fuehr auf dem n x n Gitter einen Monte-Carlo-Schritt
    am n**2 zufaellig gewaehlten Spins durch
    """
    # Anzahl der durchzufuehrenden Metropolis-Schritte
    N = n**2
    for i in range(N):
        k, l = np.random.randint(n, size=2) # Matrix-Index fuer zuf. Spins
        # Anliegende Spins (mit period. Randbed.) aufsummieren
        sum_sigma = np.sum([gitter[k, ((l+1) % n)], gitter[k, ((l-1) % n)],
                            gitter[((k+1) % n), l], gitter[((k-1) % n), l]])
        delta_H = 2 * gitter[k, l] * sum_sigma
        # Pruefen ob Spin direkt geflippt oder zufaellig geflippt wird
        if delta_H <= 0:                    # direkt geflippt (WS=1)
            gitter[k, l] = -gitter[k, l]

        else:                               # zufaellig geflippt (WS=ws_flip)
            ws_flip = np.exp(-np.abs(delta_H)/tau)
            # Es wird geprueft ob zufaellig geflippt werden muss
            if np.random.uniform() < ws_flip:
                gitter[k, l] = -gitter[k, l]

    return gitter

def mouse_klick(event):
    """Bei Linksklick in die 'Spinverteilung' werden 10 Monte-Carlo-
    Zeitschritte ausgefuehrt.
    Bei Rechtsklick in die 'Mittlere Magnetisierung' wird ein neues Ausgangs-
    Gitter mit den Klick-Koordinaten als Startparameter generiert.
    """
    global gitter, tau
    # Klick in linkes Fenster startet 10 Monte-Carlo-Schritte
    if plt.get_current_fig_manager().toolbar.mode == '' and event.button == 1\
    and event.inaxes == ax_gitter:
        for i in range(10):
            gitter = monte_carlo(gitter)    # 1 Metropolis-Schritt
            plt.setp(spins, data=gitter)    # Gitter aktualisieren
            # Phasendiagramm aktualisieren
            plt.setp(phase, xdata=tau, ydata=np.mean(gitter))
            plt.draw()
    # Klick in rechtem Fenster generiert neues Spingitter
    if plt.get_current_fig_manager().toolbar.mode == '' and event.button == 1\
    and event.inaxes == ax_phase:
        # Generieres neues Spin-Gitter mit mittlerer Magn. m = ydata und Plot
        gitter = spinzustand_neu(event.ydata, n=n)
        plt.setp(spins, data=gitter)
        # Setzte tau auf den x-Wert des Klicks
        tau = event.xdata
        # Berechne wirkliches m aus dem gen. Gitter und Ausgabe in Plot
        plt.setp(phase, xdata=tau, ydata=np.mean(gitter))
        plt.draw()


    
def main():
    """Es wird das Ising-Modell abgebildet. Die Startwerte werden zu tau = 1.5
    und m=0.8 gewaehlt.
    """
    # Benutzerfuehrung
    print __doc__
    print "Der Spin '+1' wird in rot, der Spin '-1' wird in blau dargestellt"
    # einige globale Parameter fuer Event-Funktion
    global ax_gitter, ax_phase, gitter, tau, spins, phase, n

    n = 50        # Gittergroesse
    # Ausgangswerte
    tau = 1.5     # dimensionslose Temperatur
    m = 0.8       # mittlere Magnetisierung

    # Plotbereiche anlegen
    plt.figure(0, figsize=(15,7))
    ax_gitter = plt.subplot(121)
    ax_gitter.set_title("Spinverteilung")
    
    ax_phase = plt.subplot(122)
    ax_phase.set_title("Mittlere Magnetisierung")
    ax_phase.set_xlabel(r"$\tau$")
    ax_phase.set_ylabel(r"$m$")
    ax_phase.set_xlim(0, 4)
    ax_phase.set_ylim(-1.1, 1.1)
    
    # oberen und unteren Zweig fuer analytischen Wert von m_inf zeichnen
    # bei den 
    temps = np.linspace(4, 0, 1000, endpoint=False)
    ax_phase.plot(temps, m_inf(temps), color='b', lw=2, label=r"$m_\infty$")
    ax_phase.plot(temps, -m_inf(temps), color='b', lw=2)
    ax_phase.legend(loc="upper right")

    # Ausgangs Spin-Gitter berechnen
    gitter = spinzustand_neu(m, n=n)
    # Ausgangsplots erstellen und ausgeben
    spins = ax_gitter.imshow(gitter, interpolation='nearest')
    phase = ax_phase.plot(tau, np.mean(gitter), marker='o', color='k', ms=6)
    plt.connect('button_press_event', mouse_klick)
    plt.show()
    
if __name__ == "__main__":
    main()

# tau = 1.5:
#       Der Startwert von m beeinflusst stark den Verlauf der Monte-Carlo-
#       Schritte. Desto naeher man an den zu erwartenden Werten von ca. -1/+1
#       startet, desto eher stellt sich der zu erwartende Wert auf der
#       analytischen Kurve ein. Legt man den Startwert in die Naehe von m=0 so
#       kann beobachtet werden wie der Wert sehr lange um die 0 schwankt.
#       Ein aehnliches Verhalten kann auch beobachtet werden wenn sich im
#       Spin-Gitter 'Inseln' bilden. Diese fuehren dazu, dass wenig Spins
#       flippen, da ihre umliegenden Spins ein flippen unwahrscheinlich machen.
# tau = 3:
#       Es kann beobachtet werden, dass die mittlere Magnetisierung stark
#       schwankt. Durch die sehr zufaellig verteilten Spin-Orientierung
#       ist auch das flippen der einzelnen Spins sehr zufaellig. Dadurch
#       schwankt auch der Mittelwert aller Spins entsprechend.


# Ich bekomme eine RuntimeWarning-Meldung fuer die Berechnung in Zeile 25. Ich
# bin mir nicht sicher wie der power-overflow entsteht, da ich ja eigentlich
# nur die benoetigten Werte uebergebe und die Formel ja auch richtig ueber-
# nommen sein sollte, und es scheinbar keine Beeintraechtigung beim ausfuehren
# des Programms gibt, und es auch schon recht spet ist, bin ich leider nicht
# mehr in der Lage dieses Problem zu beheben und wollte nur darauf aufmerksam
# machen das mir diese Fehlermeldung aufgefallen ist.
