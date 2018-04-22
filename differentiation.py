#!/usr/bin/python
#-*- coding: utf-8 -*-

"""Plottet potentielle, kinetische und Gesamtenergie der Punktmasse aus 
Aufgabe 4. Zur Berechnung der Kurve werden die Messwerte aus der 
Datei Bewegung.dat numerisch differenziert. Dazu werden 2 verschiedene
Methoden verwendet: einmal manuell über die Methode der zentralen
Differentiation und einmal über die eingebaute Funktion gradient() 
von Numpy."""

import numpy as np
from matplotlib import pyplot as plt
import math

messwerte = np.loadtxt("C:\Users\Nitrox\Documents\Dokumente\Skripte\py\Bewegung.dat")

"""Aufsplitten der Datei in 3 Arrays:"""
t = messwerte[:,0] #diskrete Zeitmesspunkte aus Datei
x = messwerte[:,1] #x-Koordinaten aus Datei
z = messwerte[:,2] #z-Koordinaten aus Datei
"""Konstanten:"""
m = 7.257 #Masse des Wurfkörpers
g = 9.81 #Erdbeschleunigung
"""Erstellen von leeren Arrays für Zwischenergebnisse:"""
v = [] #Geschwindigkeitsvektoren
r = [] #Ortsvektoren
v_abs = [] #Geschwindigkeitsbetrag
E_kin = [] #kinetische Energie
E_pot = [] #potentielle Energie
E_ges = [] #Gesamtenergie zur Kontrolle

v_new_abs = [] #Geschwindigkeitsbetrag der anders berechneten Geschw.
E_kin_new = [] #kinetische Energie mit np.gradient()
E_pot_new = [] #potentielle Energie mit np.gradient()
E_ges_new = [] #Gesamtenergie mit np.gradient()
v_new4 = [] #Geschwindigkeitsvektoren mit np.gradient()

# --- 1. Manuelle Berechnung der Energieverläufe

for i in range(0, len(t)):
	"""Iteriert durch den Datensatz und füllt Array r mit Ortsvektoren."""
	r.append([x[i], z[i]])

"""Iteriert durch das so eben erzeugte Array r und berechnet jeweils die
Geschwindigkeit über zentrale Differentiation. Für den Anfangs- und den 
Endpunkt muss man sich über die lineare Interpolation nach vorne bzw. 
hinten behelfen."""
for i in range(0, len(t)):
		if i < 1:
			v.append( ( np.array(r[1]) - np.array(r[0]) ) / ( t[1] - t[0] ) )
			i = i+1
		elif i > 0 and i < (len(t)-1):
			v.append( ( np.array(r[i+1]) - np.array(r[i-1]) ) / ( t[i+1] - t[i-1] ) )
			i = i+1
		else:
			v.append( ( np.array(r[len(t)-1]) - np.array(r[len(t)-2]) ) / ( t[len(t)-1] - t[len(t)-2] ) )

for i in range(0, len(t)):
	"""Berechnet jeweils den Betrag der Geschwindigkeitsvektoren mittels
	eingebauter Funktion."""
	v_abs.append(np.linalg.norm(v[i]))

for i in range(0, len(t)):
	"""Berechnet kinetische Energie mit Geschwindigkeitsbetrag von oben."""
	E_kin.append(0.5 * m * (v_abs[i])**2)

for i in range(0, len(t)):
	"""Berechnet potentielle Energie aus z-Koordinate (aus Datei) und
	Konstanten."""
	E_pot.append(m * g * z[i])

for i in range(0, len(t)):
	"""Addiert kinetische und potentielle Energie; wegen Energieerhaltung
	sollte das im Plot eine Gerade werden."""
	E_ges.append(E_kin[i] + E_pot[i])

"""Plottet die drei Energien mit Legende, Titel und Gitternetz. 
Eine y-Achse reicht diesmal, da die Einheiten und die Skaleneinteilung 
gleich sind (Energie in Joule)."""
fig, ax = plt.subplots()
ax.plot(t, E_kin, 'b', label='kinetische Energie') #Verlauf der kinetischen Energie
ax.plot(t, E_pot, 'b:',label='potentielle Energie') #Verlauf der potentiellen Energie
ax.plot(t, E_ges, 'b--', label='Gesamtenergie') #Verlauf der Gesamtenergie
plt.xlabel('Zeit in $s$')
plt.ylabel('Energie in $J$')
fig.suptitle('Manuell berechnete Energien', fontsize=16)
ax.legend(loc='lower center', shadow=True) #Legende
ax.grid()


# --- 2. Differentiation mit np.gradient()
"""np.gradient() ist eine eingebaute Funktion, die in einem Numpy-Array
mittels zentraler Differentiation (eigentlich genauso wie oben)
differenziert."""

dt = t[1] - t[0] #Samplingabstand: Zeitabstand zwischen 2 Messpunkten

v_new = np.gradient(np.array([x,z]), dt) #np.gradient() erzeugt Array
#mit den numerischen Ableitungen an jedem Messpunkt.

"""Die folgenden Umformungen sind zwar etwas unschön, bringen das von
np.gradient() erzeugte Array in die gleiche Form wie das Array v."""
v_new2 = np.delete(v_new, 0, 0)
v_new3 = np.array(v_new2[0])
v_new_x = np.array(v_new3[0])
v_new_z = np.array(v_new3[1])

for i in range(0, len(t)):
	v_new4.append([v_new_x[i], v_new_z[i]])

for i in range(0, len(t)):
	"""Jetzt kann von jedem Geschwindigkeitsvektor wieder der Betrag
	berechnet werden."""
	v_new_abs.append(np.linalg.norm(v_new4[i]))

for i in range(0, len(t)):
	"""Danach die kinetische Energie, analog zu oben."""
	E_kin_new.append(0.5 * m * (v_new_abs[i])**2)

for i in range(0, len(t)):
	"""Ebenso die potentielle Energie."""
	E_pot_new.append(m * g * z[i])

for i in range(0, len(t)):
	"""Und zum Schluss (Kontrolle) noch einmal die Gesamtenergie."""
	E_ges_new.append(E_kin_new[i] + E_pot_new[i])

"""Zuletzt werden diese Energieverläufe in einem neuen Diagramm geplottet.
Zur Unterscheidung sind die Linien unterschiedlich gezeichnet, mit einer
Legende versehen und die Diagramme beschriftet. Wie erwartet sehen beide
Energieverläufe gleich aus, was bedeutet, das np.gradient() genauso
arbeitet, wie die manuelle Methode."""
fig2, ax2 = plt.subplots()
ax2.plot(t, E_kin_new, 'k', label='kinetische Energie') #Verlauf der kinetischen Energie
ax2.plot(t, E_pot_new, 'k:',label='potentielle Energie') #Verlauf der potentiellen Energie
ax2.plot(t, E_ges_new, 'k--', label='Gesamtenergie') #Verlauf der Gesamtenergie
plt.xlabel('Zeit in $s$')
plt.ylabel('Energie in $J$')
fig2.suptitle('Energien mit numpy.gradient()', fontsize=16)
ax2.legend(loc='lower center', shadow=True) #Legende
ax2.grid()
plt.show()
