#! /usr/bin/env python

"""Uebung 9: Diffusion mit Drift und Absorption

Mit diesem Programm wird ein Diffusionsvorgang mit Drift und Absorption unter
der Verwendung der Langevin-Gleichung simuliert.
Es besteht die Moeglichkeit nach Berechnung der entsprechenden Werte die
Aufenthaltsorte der Teilchen und die Entwicklung wichtiger statistischer
Groessen dynamisch zu verfolgen.
"""

from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import mlab as mlab
import time


def orte_plot(zeiten, x0, v_drift, diff_const, x_abs, plot_intervall):
    """Diese Funktion berechnet mit Hilfe der Langevin-Gleichung die
    Aufenthaltsorte eines Teilchens zu einzelnen Zeiten. Es werden Drift,
    Diffusion, und Absorption an einer Kante beruecksichtigt.
    Es wird nur jeder 'plot_intervall'-te Ort zurueck gegeben, da spaeter nur
    diese Werte zur dynamischen Ausgabe verwendet werden.
    Parameter:
        zeiten        : Array von Zeiten
        x0            : Ausgangsort des Teilchens
        v_drift       : Driftgeschw.
        diff_const    : Diffusionskonst.
        x_abs         : Ort der Absorptionskante
        plot_intervall: Jeder plot_intervall-te Ortswert wird zurueckgegeben
    Rueckgabe:
        x : Array mit Ortskoordinate
    """
    N = len(zeiten)                     # Anzahl der zu berechnenden Zeitpunkte
    dt = zeiten[1] - zeiten[0]          # Zeitschrittweite
    diff_term = np.sqrt(2*diff_const*dt) * np.random.randn(N-1)
    x = np.empty(N)                     # Ortsarray anlegen
    x[0] = x0                           # Ausgangsort festlegen
    # Langevin - Gleichung:
    for i in (np.arange(N-1)+1):
            x[i] = x[i-1] + v_drift * dt + diff_term[i -1]
            if x[i] >= x_abs:           # Abs. Teilchen werden zu x_abs + 1
                x[i:] = x_abs +1        # gesetzt
                break
    x = x[::plot_intervall]     
    return x

def verteilung_theorie(x, t_plot, x0, v_drift, diff_const, x_abs):
    """Diese Funktion liefert die theoretisch zu erwartenden Aufenthalt-
    wahrscheinlichkeit p(x,t) in Abhaengigkeit von Ort und Zeit eines Teilchens
    zurueck. Die Formeln ergeben sich aus der Loesung der Fokker-Planck-Gl. und
    sind mit und ohne abs. Rand realisiert.
    Parameter:
        x             : Ortspunkte fuer die Aufenthaltswahrsch. berechnet wird
        t_plot        : Array von Zeiten
        x0            : Ausgangsort des Teilchens
        v_drift       : Driftgeschw.
        diff_const    : Diffusionskonst.
        x_abs         : Ort der Absorptionskante
    Rueckgabe:
        orte_theorie    : 2-dim Array mit Aufenthalswahrscheinlichkeiten zu
                          den Zeiten t_plot, ohne abs. Rand
        orte_theorie_abs: 2-dim Array mit Aufenthalswahrscheinlichkeiten zu
                          den Zeiten t_plot, mit abs. Rand
    """
    zeitpunkte = len(t_plot)
    ortspunkte = len(x)
    drift = v_drift * t_plot
    sigma = np.sqrt(2 * diff_const * t_plot)
    orte_theorie = np.zeros(shape=(zeitpunkte, ortspunkte))
    orte_theorie_abs = np.zeros(shape=(zeitpunkte, ortspunkte))
    # Der Zeitpunkt t=0 wird ausgeschlossen (varianz=0 problematisch)
    for i in np.arange(1, zeitpunkte):
            orte_theorie[i,:] = mlab.normpdf(x, x0 + drift[i], sigma[i])
    for i in np.arange(1, zeitpunkte):
        orte_theorie_abs[i,:] = ((mlab.normpdf(x, x0 + drift[i], sigma[i])) -
                    (mlab.normpdf(x, 2 * x_abs - x0 + drift[i], sigma[i])) *
                    (mlab.normpdf(x_abs, x0 + drift[i], sigma[i])) /
                    (mlab.normpdf(x_abs, 2 * x_abs - x0 + drift[i], sigma[i])))
    return orte_theorie, orte_theorie_abs


def statistik(teilchen, x_abs):
    """Diese Funktion berechnet ausgehend von der Ortsverteilung der Teilchen
    die Statistischen Werte Mittelwert und Varianz dieser Verteilungen aus.
    Ausserdem wird das Verhaeltnis der erhaltenen Teilchen zu den Startteilchen
    als Norm zurueckgegeben.
    Parameter:
     teilchen : 2-dim Array von Ortsverteilungen zu versch. Zeiten
     x_abs    : Lage des absorbierenden Randes
    Ruckgabe:
     erwartung: Array mit den Mittelwerten der Ortsverteilung zu versch. Zeiten
     varianz  : Array mit den Varianzen der Ortsverteilung zu versch. Zeiten
     norm     : Verhaeltnis der erhaltenen Teilchen zur Anfangsanzahl
    """
    count = len(teilchen[0, :])
    R     = len(teilchen[:, 0])
    erwartung = np.empty(count)
    varianz   = np.empty(count)
    norm      = np.empty(count)
    for i in range(count):
        orte = teilchen[:, i]
        orte = orte[orte < x_abs]
        erwartung[i] = np.mean(orte)
        varianz[i]   = np.var(orte, ddof=1)
        norm[i]      = len(orte)/R
    return erwartung, varianz, norm
    

def plot_animation(event):
    """Bei Klick in das Histogramm-Fenster wird der Zeitverlauf ausgegeben.
    Es werden geplottet:
    - Theoretisch zu erwartende Verteilung (mit und ohne abs. Rand)
    - Verlauf vom Norm, Erwartungswert, Varianz
    """
    # Pruefen ob richtiger Plotbereich geklickt
    if plt.get_current_fig_manager().toolbar.mode == '' and event.button == 1\
    and event.inaxes == hist:
        count = len(T_plot)
        # Plots fuer t=0 erstellen
        hist_wert, kanten = np.histogram(teilchen[:,0], bins=bins, density=True)
        breite = np.diff(kanten)
        hist_wert = hist_wert * norm_werte[0]

        hist.bar(kanten[:-1], hist_wert, breite, color = "b")
        norm_kurve = norm.plot(T_plot[0], norm_werte[0], color="b")
        erwartung_kurve = erwartung.plot(T_plot[0], erwartung_werte[0],
                                                                    color="b")
        varianz_kurve = varianz.plot(T_plot[0], varianz_werte[0], color="b")

        # Fuer Zeiten t > 0 dynamsicher Plot
        for i in np.arange(1, count):
            hist.patches = []           # Histogramm - Plotbereich leeren
            hist.lines   = []
            orte = teilchen[:,i]
            orte = orte[orte < x_abs]   # Nicht abs. Teilchen bestimmen
            hist_wert, kanten = np.histogram(orte, bins=bins, density=True)
            breite = np.diff(kanten)                # Histogramm erstellen
            hist_wert = hist_wert * norm_werte[i]   # und reskalieren
            hist.bar(kanten[:-1], hist_wert, breite, color = "b")
            # Theoretische Vorhersage ausgeben
            hist.plot(x_th, orte_theorie[i-1,:], color ="k", linewidth=2,
                                                label="theoretisch ohne abs.")
            hist.plot(x_th, orte_theorie_abs[i-1,:], color ="c", linewidth=2,
                                                label="theoretisch mit abs.")
            hist.legend()

            # Statistische Kenngroessen ausgeben
            plt.setp(norm_kurve[0], xdata=T_plot[:i], ydata=norm_werte[:i],
                                                                    color="b")
            plt.setp(erwartung_kurve[0], xdata=T_plot[:i],
                                         ydata=erwartung_werte[:i], color="b")
            plt.setp(varianz_kurve[0], xdata=T_plot[:i],
                                         ydata=varianz_werte[:i], color="b")

            plt.draw()
            time.sleep(0.2)


def main():
    """Es werden zunaechst die wichtigsten Parameter des Problems festgelegt
    und anschliessend die Ortsverteilungen mit den entsprechenden Funktionen
    berechnet. Anschliessend werden die statistischen Auswertungen vorgenommen
    und die grafische Ausgabe vorbereitet und die theoretisch zu erwartenden
    Verlaeufe der statistischen Groessen ausgegeben.
    """
    # Benutzerfuehrung
    print __doc__
    # Benoetigte Parameter (einige global, da event-funktion):
    global T_plot, hist, norm, erwartung, varianz,erwartung_werte, x_abs, x_th
    global varianz_werte, norm_werte, bins, orte_theorie, orte_theorie_abs
    global teilchen
    # Zeitparameter
    T0    = 0
    T_max = 40
    dt    = 0.01
    N     = (T_max - T0)/dt +1
    T     = np.linspace(T0, T_max, N)
    plot_intervall = 100
    T_plot = T[::plot_intervall]

    # Parameter der Teilchen
    x0         = 0
    v_drift    = 0.15
    diff_const = 1.5
    x_abs      = 15
    R          = 10**4
    # Histogrammparameter
    bins = 20
    
    
    # Berechnung fuer mehrere Realisierungen und Benutzerinformation
    print "Nach der Berechnung besteht die Moeglichkeit einer dyn. Simulation!"
    print "Starte Berechnung von", R, "Teilchen:"
    # Array zur Speicherung der Werte mit und ohne abs. Rand:
    teilchen = np.empty(shape=(R,((len(T)/plot_intervall)+1)))
                                              
    for i in range(R):
        teilchen[i,:] = orte_plot(T, x0, v_drift,
                                            diff_const, x_abs, plot_intervall)
        if (i+1) % 1000 == 0:
            print i+1, "Teilchen berechnet."

    # Statistische Auswertung der simulierten Teilchen        
    erwartung_werte, varianz_werte, norm_werte = statistik(teilchen, x_abs)

    # Theoretische Vorhersagen bestimmen
    x_th = np.linspace(-20,20, 1000)
    orte_theorie, orte_theorie_abs = verteilung_theorie(x_th, T_plot, x0,
                                                    v_drift, diff_const, x_abs)
 
    print "Berechnungen beendet!"
    print "Sie koennen jetzt die Simulation mit Klick in das Diagramm oben \
            links starten"

    
    # Plotbereiche anlegen
    figure = plt.figure(0, figsize=(14,9))
    figure.subplots_adjust(wspace=.3, hspace=.4)
    
    hist = plt.subplot(221)
    hist.set_title("Ortsverteilung der Teilchen")
    hist.set_xlabel(r"$x$")
    hist.set_ylabel("Wahrscheinlichkeit")
    hist.set_xlim(-20,20)
    hist.set_ylim(0, .1)

    norm = plt.subplot(222)
    norm.set_title(r"Normierungsfaktor R(t_n)/R")
    norm.set_xlabel(r"$t$")
    norm.set_ylabel("Norm")
    norm.set_xlim(T0, T_max)
    norm.set_ylim(np.min(norm_werte), 1.1)

    erwartung = plt.subplot(223)
    erwartung.set_title("Erwartungswert")
    erwartung.set_xlabel(r"$t$")
    erwartung.set_ylabel("Erwartungswert")
    erwartung.set_xlim(T0, T_max)
    erwartung.set_ylim(0, np.max(erwartung_werte))

    varianz = plt.subplot(224)
    varianz.set_title("Varianz")
    varianz.set_xlabel(r"$t$")
    varianz.set_ylabel("Varianz")
    varianz.set_xlim(T0, T_max)
    varianz.set_ylim(0, np.max(varianz_werte))

    # Theoretische Werte ausgeben
    norm.axhline(1, T0, T_max, label = "theoretisch, ohne abs.",
                                                              color = "black")
    norm.legend(loc="lower left")
    erwartung.plot(T_plot, x0 + v_drift * T_plot,
                            label = "theoretisch, ohne abs.", color = "black")
    erwartung.legend(loc="lower right")
    varianz.plot(T_plot, 2 * diff_const * T_plot,
                            label = "theoretisch, ohne abs.", color = "black")
    varianz.legend(loc="lower right")
    
    plt.connect('button_press_event', plot_animation)
    plt.show()

if __name__ == "__main__":
    main()

#   a) Betrachtet man die einzelnen Groessen so stellt man fest das bei allen
#      eine Veraenderung zum theoretischen Wert ab ca. t=6 auftritt. Dieses
#      Verhalten faengt bei allen betrachteten Groessen zur selben Zeit an, da
#      es auf der Absorption der Teilchen an der abs. Kante beruht und diese
#      natuerlich fuer alle Groessen zur gleichen Zeit auswirkungen zeigt.
#      Erwartungswert: Da sich die Teilchen im mittel nach v_drift * t bewegen,
#           wie auch der theoretische Wert zeigt, bewegen ist zu erwarten, dass
#           sich der Erwartungswert in pos. Richtung verschiebt. Treffen jedoch
#           die ersten Teilchen auf den abs. Rand, so fehlen diese am rechten
#           Rand und die Teilchen links fallen daher staerker ins Gewicht und
#           verschieben den Erwartungswert daher wieder leicht nach unten.
#      Varianz: Ensprechend der Erwartung waechst die Varianz zunaechstlinear 
#           nach 2 * diff_const * t. Werden die ersten Teilchen absorbiert, so
#           koennen diese nicht weiter 'auseinanderlaufen' wie man bis ca. t=6
#           beobachten kann. Da diese Teilchen also nicht ueber den Wert von
#           x_abs gelangen koennen und sich die Teilchen ganz links durch den
#           Drift langfristig nach rechts gezwungen werden, wird die Verteilung
#           etwas 'zusammen geschoben', weshalb die Varianz und damit auch die
#           Breite nicht so stark wie theoretisch, ohne abs., zu erwarten waere
#      Norm: Bis ca. t=6 bleibt die Norm konstant bei 1, da noch keine Teilchen
#           absorbiert wurden. Da die Teilchenbewegung durch den Drift
#           dominiert wird, und dieser einer linearen Translation entspicht,
#           verhaelt sich auch die Norm in gleichem Masse linear und faellt
#           stetig ab.
#
#   b)      Man beobachtet keine deutliche Veraenderung. Den groessten
#           Unterschied kann man beim Erwartungswert beobachten. Da man nun nur
#           noch 40 anstatt zufaellige Ereignisse hat, koennen mehr Teilchen
#           nach links diffundieren und daher der Absorption entkommen, bei der
#           Aufgabe a) wurden so viele Zufallsereignisse betrachtet, dass hier
#           der Zufall, bzw. die zufaellige Gewichtung kaum noch eine Rolle
#           gespielt hat.
#
#   c) Betrachtet man eine erhoete Driftgeschw. von v_drift = 0.5 so verhalten
#           sich die Kurven qualitativ aehnlich zu Aufgabe a) da hier die
#           immer noch die selben Grundideen anwendung finden. Durch den
#           erhoeten Drift bilden sich jedoch quantitative Unterschiede aus.
#      Erwartungswert: Der Erwartungswert steigt im Gegensatz zu a). Dies liegt
#           daran, dass Teilchen, die zuvor nach links diffundieren konnten,
#           jetzt durch den erhoeten Drift auch nach rechts gezwungen werden.
#           Es wandern also mehr Teilchen nach recht als in a) wes in einem
#           groesserm Erwartungswert resultiert.
#      Varianz: Die Varianz verringert sich im Vergleich mit a). Dieses
#           Verhalten kann aehnlich zum Erwartungswert erklaert werden. Da sich
#           mehr Teilchen weiter rechts als in a) befinden wird die Breite der
#           Verteilung schmaler, da sich links deutlich weniger Teilchen
#           befinden.
#      Norm: Die Norm faellt deutlich schneller als fuer v_drift = 0.15, da
#           die Teilchen staerker nach rechts gezwungen werden als in a)
#           erreichen natuerlich auch mehr die Absorpionskante und verschwinden
#           daher. 
