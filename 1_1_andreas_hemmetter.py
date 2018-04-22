#-*- coding: utf-8 -*-

u"""Dieses Programm plottet den Phasenraum eines gekickten Rotors mit
periodischen Randbedingungen in Winkel und Impuls (Torus). Als einziger
freier Parameter geht die Kickstärke K ein, deren Wert das Verhalten
des Systems bestimmt. Im Bereich K > 0 verhält es sich zunehmends
chaotisch, während es bei K = 0 die Phasenraumtrajektorie des
ungekickten Rotors beschreibt. Durch einen Linksklick in den Phasenraum
werden neue Anfangswerte theta und p ausgewählt und ein neuer
Orbit gestartet. Das Programm startet für K = 2.6.
Andreas Hemmetter, 3957650"""

print __file__                                  # Dateiname
print __doc__                                   # Benutzerführung

import numpy as np								# Importbefehle	
from matplotlib import pyplot as plt
from random import randint						# für zufällige Farbwahl

def orbit(theta=0.0, p=0.0):
    """Hauptteil, Iteration über 1000 Kicks. Winkel und Impuls
    werden laut Angabe berechnet (mit periodischen Randbedingungen
	für Winkel und Impuls) und anschließend in 2 Arrays gespeichert 
    und geplottet."""
    
    K = 2.6					                    # Kickstärke
    x_array = []
    y_array = []
    kicks = np.linspace(1, 1000, 1000)          # Anzahl der Kicks

    for n in kicks:
        # Iteration über die 1000 Kicks pro Orbit
        theta = (theta + p) % (2*np.pi)
        p = (p + K * np.sin(theta) + np.pi) % (2*np.pi) - np.pi
        # Implementierung der periodischen Randbedingungen
        x_array.append(theta)
        y_array.append(p)
    return x_array, y_array

def onclick(event):
    """Klickposition beschreiben neue Startwerte. 
	Koordinaten für 1000 Iterationen werden in 2 Arrays geschrieben. 
    Bei jedem Klick wird eine zufällige Farbe aus dem farben-Array 
    ausgewählt und der Plot damit neugezeichnet."""
    
    # Array mit etwas schöneren Farben (zum Zeichnen wird eine
    # zufällige Farbe ausgewählt)
    farben = ["#588C73", "#F2E394", "#F2AE72", "#D96459", "#8C4646"]
    mode = plt.get_current_fig_manager().toolbar.mode
    if mode == "":
		# Abfrage, ob sich das Fenster im Zoommodus befindet. Falls
		# nein, kann der neue Orbit gestartet werden.
        theta, p = event.xdata, event.ydata     # Klick-Koordinaten
        x_array, y_array = orbit(theta, p)
        farbe = farben[randint(0,4)]            # zufällige Farbe
        plt.plot(x_array, y_array, farbe, marker=".", linestyle="none",
        markersize=1)                           # Plotbefehl
        plt.draw()

def main():
    """Mainfunktion. Initialisiert das Plotfenster und definiert, wie
    der Benutzer mit dem Fenster interagieren kann."""
    
    plt.connect('button_press_event', onclick)  # Klickabfrage
    plt.subplot(111, aspect=1.0)                # quadratisches Fenster
    plt.title("Gekickter Rotor")
    plt.xlabel(r"$\theta$")
    plt.ylabel("$p$")
    plt.axis([0.0, 2*np.pi, -np.pi, np.pi])     # relevanter Ausschnitt
    plt.show()

if __name__ == "__main__":
	main()

# Beobachtungen: es bilden sich Inseln mit stabilen Orbits. Bei kleinen
# Anregungen (um den Nullpunkt) laufen stabile Orbits, diese Bereiche 
# werden kleiner, je höher die Kickstärke gewählt wird. Im Spezialfall 
# K = 0 zeigen sich nur Linien (freier Rotor). Die anfänglichen Ellipsen 
# verformen sich mit wachsender Kickstärke und bilden neue, getrennte 
# Inseln. Bei näherem Hinzoomen an die Grenze zwischen solch einer Insel 
# und einer chaotischen Trajektorie findet man einen schlagartigen 
# Übergang zum anderen Regime, das System hängt also sensitiv von den 
# Anfangsparametern ab; diese entscheiden, ob es sich regulär oder 
# chaotisch verhält.
