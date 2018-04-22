#! /usr/bin/env python

"""
Es wird die Dynamik eines freien Teilchens in einem angetriebenen Doppelmulden-
Potential betrachtet. Hierzu wird die zugehoerige Hamiltonfunktion:

        H(x,p,t) = p**2/2 + x**4 - x**2 + x(A + B*sin(omega*t))

numerisch mit der in scipy integrierten 'odeint'-Funktion geloest. Die daraus
ermittelte Bewegung wird in 2 Phasenraumdiagrammen abgebildet. Eine
kontinuierliche Trajektorie und eine stroboskopische, bei der nur die
Koordinaten nach einer vollen Periode abgebildet werden.

Hier werden jeweils die Bewegung ueber 200 Perioden abgebildet. Es ist
ausserdem moeglich durch Links-Klick in ein beliebiges Phasenraumdiagramm einen
neuen Plot mit den geklickten Startwerten auszugeben.
In dem kontinuierlichen Phasenraumdiagramm sind ausserdem 8 Konturlinien fuer
Energien zwischen aus [-0.3, 1.5] abgebildet.
"""

from __future__ import division
import numpy as np
from scipy.integrate import odeint
from matplotlib import pyplot as plt

def rechteSeite(y, t, A=0.1, B=0.1, omega=1):
    """
    Rechte Seite der DGL des Pendels.

    Hierbei ist y = [x, p] ein Vektor im Phasenraum.
    A, B und omega sind Parameter.
    """
    return np.array([y[1], -4 * y[0]**3 + 2*y[0] - A - B * np.sin(omega * t)])


def mouse_click(event, A=0.1, B=0.1, omega=1):
    """
    Diese Funktion uebernimmt bei einem Linksklick in eines der beiden
    Diagramme den Ort des Linksklicks als Startbedingungen und zeichnet davon
    ausgehend sowohl einen kontinuierlichen und einen stroboskopischen Plot
    in das entsprechende Diagramm.
    """
    # Fenstermodus des Ausgabefensters
    mode = plt.get_current_fig_manager().toolbar.mode
    # Prueft ob Zoom deaktiviert ist und ob mit links geklickt wird
    if event.button == 1 and event.inaxes and mode == '':
        y_t = odeint(rechteSeite, [event.xdata,event.ydata],
        t, args=(A,B,omega))                    # Berechnung der Koordinaten
        x_t= y_t[:, 0]                          # x-Koordinaten
        p_t= y_t[:, 1]                          # y-Koordinaten
        ax_traject.plot(x_t, p_t,)              # Kontinuierlicher Plot
        ax_strob.plot(x_t[::steps], p_t[::steps],ls="none", marker=".",
        markersize=1)                           # Stroboskopischer Plot
        plt.draw()

# Benutzerfuehrung durch Docstring
print __doc__

# Parameter zur Berechnung der Teilchentrajektorie
A       = 0.1            # Parameter der Hamiltonfkt
periods = 200            # Perioden
steps   = 40             # Schritte pro Periode
omega   = 1              # Kreisfrequenz

# Array der Zeiten t  fuer 200 Perioden mit 'steps' Schritten pro Periode
t = np.linspace(0, 2*np.pi*periods/omega, periods*steps +1)

# Grenzen der Diagramm-Bereiche festlegen
x_lim = 1.5                # |x| der Phasenraumdiagramme
p_lim = 2                  # |p| der Phasenraumdiagramme


# Parameter und Koordinaten zum Zeichnen der Konturlinien
N     = 100                                # Teilung des Grid fuer Konturlinien
x_arr = np.linspace(-x_lim, x_lim, N)      # 1D X Werte
p_arr = np.linspace(-p_lim, p_lim, N)      # 1D Y Werte
x2d, p2d = np.meshgrid(x_arr, p_arr)       # 2D X und Y Werte
H = p2d**2/2 + x2d**4 - x2d**2 + x2d*A     # Hamiltonfkt
energien = [-0.3, -0.1, -0.05, 0, 0.2, 0.55, 0.75, 1.5]


# Stationaeres Doppelmulden Potential in extra Fenster
plt.figure(0)
plt.title("Stationaeres Doppelmuldenpotential (t=0)")
plt.xlabel("x")
plt.ylabel("p")
x = np.linspace(-1, 1, 1000)
plt.plot(x, x**4 - x**2 + 0.1*x)

# Anlegen des Ausgabefensters der Phasenraumdiagramme
plt.figure(1, figsize=(16, 10))
ax_traject = plt.subplot(121)
ax_strob   = plt.subplot(122)
# Kontinuierliches Diagramm
ax_traject.set_title("Trajektorie des Teilchens")
ax_traject.set_xlabel("x")
ax_traject.set_ylabel("p")
ax_traject.axis([-x_lim, x_lim, -p_lim, p_lim])
# Stroboskopisches Diagramm
ax_strob.set_title("Stroboskopische Darstellung der Teilchentrajektorie")
ax_strob.set_xlabel("x")
ax_strob.set_ylabel("p")
ax_strob.axis([-x_lim, x_lim, -p_lim, p_lim])

# Mausabfrage und Ausgabe der Grafik
ax_traject.contour(x2d, p2d, H, energien,               # Konturlinien fuer
        colors='black', linestyles='solid')             # ausgewaehlte Energien
ax_strob.contour(x2d, p2d, H, energien,               # Konturlinien fuer
        colors='black', linestyles='solid')             # ausgewaehlte Energien
plt.connect('button_press_event', mouse_click)
plt.show()



# Aufgaben:
# 
#   a) Da die Energie bzw. die Hamiltonfunktion zeitlich konstant ist und fuer
#      -/+ Unendlich gegen Unendlich geht, erwartet man eine Bewegung des 
#      Teilchens entlang einer Konturlinie. Das Teilchen muss sich also auf 
#      geschlossenen Bahnen bewegen.
#
#   b) Im Ortsraum entspricht dieses einer Bahn welche immer wieder durch die
#      gleichen Punkte lauft. Es bewegt sich auf einer speziellen Hoehe im
#      Doppelmuldenpotential. Es bildet sich eine stehende Trajektorie im
#      Doppelmuldenpotential.
#
#   c) Die Bewegung verlaeuft sehr grob in der Form der Konturlinien. Die
#      Bewegung ist jedoch sehr stark verzerrt. Das liegt an der zeitlich
#      Variablem Energie des Teilchens welche es zwischen verschiedenen Hoehen
#      im Doppelmuldenpotential "hin und her zieht". Daher bewegt es sich immer
#      kurzzeitig (fuer einen Zeitschritt) auf einer anderen Konturlinie.
#      Die Verzerrung wird besonders deutlich wenn man den Startpunkt zwischen
#      ca. der 4. - 6. Kontrulinie von aussen waehlt, da hier das System am
#      empfindlichsten ist
#
#   d) x(0) =  0.666
#      p(0) = -0.036

