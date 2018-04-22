#-*- coding: utf-8 -*-

"""Programm benutzt Daten des Versuchs FA Fehleranalyse, um aus 700
gesammelten Pendeldauern verschiedene statistische Werte zu berechnen.
Mittelwert, Standardabweichung, Standardabweichung des Mittelwerts und
deren Entwicklung mit jedem neuen Messwert wird anschließend mit
matplotlib dargestellt. """

import numpy as np
from matplotlib import pyplot as plt
import math

messwerte = np.loadtxt('/home/nitrox/Documents/Pendel-Messung.dat')

"""Berechnung des Mittelwerts mittels np.mean()."""
mittelwert = messwerte.mean()
print mittelwert

"""Berechnung der Varianz des Datensatzes. Eingebaute Funktion von numpy
kann nicht verwendet werden, da der Vorfaktor als 1/N und nicht als 
1/(N-1) gespeichert ist."""
varianz_zwwert = (messwerte - mittelwert)**2
varianz_array = 1./( len(messwerte) - 1) * varianz_zwwert.sum()
varianz = varianz_array.sum()
print varianz

"""Berechnung der Standardabweichung des Mittelwerts."""
standardabweichung_mittelwert = varianz/len(messwerte)
print standardabweichung_mittelwert

#Erzeugt einige Variablen und leere Arrays für Aufgabe 2
summe = 0
quadrate = 0
varianz2 = []
mittelwert2 = []
standardabweichung2 = []
standardabweichung_mittelwert2 = []

"""Iteration berechnet für jeden neuen Messwert jeweils den bis dahin
erreichten Mittelwert, Varianz und Standardabweichung des Mittelwertes.
"""
for i in range(1, len(messwerte)+1):
	summe += messwerte[i - 1]
	quadrate += (messwerte[i - 1])**2
	mittelwert2.append(summe / i)
	varianz2.append((quadrate - summe**2 / i) / (i - 1))
	standardabweichung2.append(math.sqrt(varianz2[i-1]))
	standardabweichung_mittelwert2.append(standardabweichung2[i-1]/math.sqrt(i))

mean = np.array(mittelwert2)
std_mean = np.array(standardabweichung_mittelwert2)

"""Plottet Ergebnisse aus Aufgabe 2 mit pyplot."""
plt.subplot(311)
plt.plot(messwerte, "b", mean - std_mean, "g", mean + std_mean, "g", mean, "r")
plt.xlabel(u"Anzahl der Messwerte")
plt.ylabel(r"Periodendauer in $s$")

"""Legt bins für das Histogramm fest."""
n = math.ceil(math.sqrt(len(messwerte) + 1))
histo, bin_edges = np.histogram(messwerte, n)
bin_left = np.delete(bin_edges, -1)

"""Plottet absolute Häufigkeitsverteilung mit Unsicherheiten."""
plt.subplot(312)
plt.bar(bin_left, histo, width=0.02)
plt.errorbar(bin_left + 0.01, histo, np.sqrt(histo), fmt="y.", ecolor="r")
plt.xlabel(r"Periodendauer in $s$")
plt.ylabel("Anzahl")

histo = histo / float(len(messwerte) + 1)

"""Plottet relative Häufigkeitsverteilung mit Unsicherheiten."""
plt.subplot(313)
plt.bar(bin_left, histo, width=0.02)
plt.errorbar(bin_left + 0.01, histo, np.sqrt(histo) / 100.0, fmt="y.", ecolor="r")
plt.xlabel(r"Periodendauer in $s$")
plt.ylabel("Anteil")

plt.show()
