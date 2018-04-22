#-*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
from random import randint

"""
Dieses Programm plottet den Phasenraum eines gekickten Rotors mit
periodischen Randbedingungen in Winkel und Impuls (Torus). Als einziger
freier Parameter geht die Kickstärke K ein, deren Wert das Verhalten
des Systems bestimmt. Im Bereich K > 0 verhält es sich zunehmends
chaotisch, während es bei K = 0 die Phasenraumtrajektorie des
ungekickten Rotors beschreibt. Durch einen Klick in den Phasenraum
werden neue Anfangswerte theta_0 und p_0 ausgewählt und ein neuer
Orbit gestartet.
Andreas Hemmetter, 3957650
"""

#---Variablen und Arrays---

K = 2.6 #Kickstärke
theta = 0
p = 0
farbe = "k" #einfache Startfarbe
x_array = []
y_array = []
kicks = np.linspace(1, 1000, 1000)
farben = ["#588C73", "#F2E394", "#F2AE72", "#D96459", "#8C4646"]

#---Standardabbildung---

def onclick(event):
	"""Konvertiert Klickposition in neue Startwerte und schreibt (kart.)
	Koordinaten für 1000 Iterationen in 2 Arrays. Bei jedem Klick wird
	eine zufällige Farbe aus dem farben-Array asgewählt und der Plot
	damit neugezeichnet (zusätzlich zu den alten)."""
	mode = plt.get_current_fig_manager().toolbar.mode
	if mode == "":
		"""Abfrage, ob sich das Fenster im Zoommodus befindet. Falls
		nein, kann der neue Orbit gestartet werden."""
		x_array = [] #setzt Arrays zurück (somit sind immer nur
		y_array = [] #1000 Einträge in jedem Array
		
		theta, p = event.xdata, event.ydata #Klick-Koord.
		
		for n in kicks:
			"""Hauptteil, Iteration über 1000 Kicks. Winkel und Radius
			werden laut Angabe berechnet (mit periodischen Randbed.
			für Winkel und Radius) und anschließend in kart. Koord.
			umgewandelt, in 2 Arrays gespeichert und geplottet."""
			theta = (theta + p) % (2*np.pi)
			p = (p + K * np.sin(theta) + np.pi) % (2*np.pi) - np.pi
			x_array.append(theta)
			y_array.append(p)
		farbe = farben[randint(0,4)] #wählt zufällige Farbe aus
		plt.plot(x_array, y_array, farbe, alpha=0.8, linewidth=0.2) #Plotbefehl
		#leichte Transparenz, um dahinterliegende Orbits zu erkennen
		plt.draw()


#---Plotbefehle---

plt.connect('button_press_event', onclick) #Abfrage, ob geklickt wurde
plt.subplot(111, aspect=1.0) #quadratisches Plotfenster
plt.plot(x_array, y_array, farbe, alpha=0.8, linewidth=0.2) #eigentlicher Plot
plt.title("Gekickter Rotor mit K = 2,6")
plt.xlabel("$\Theta$")
plt.ylabel("$p$")
plt.axis([0.0, 2*np.pi, -np.pi, np.pi]) #relevanter Ausschnitt
plt.show()

