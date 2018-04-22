#-*- coding: utf-8 -*-

"""Dieses Programm löst die Bewegungsgleichung für den Hamiltonian

H(x,p,t) = p**2/2 + x**4 - x**2 + x(A + B*sin(omega*t))

unter Zuhilfenahme der scipy-Funktion odeint. Geplottet werden die 
Trajektorien im Phasenraum bei beliebiger Wahl der Anfangsorte und 
-impulse (durch Klick ins Plotfenster).  Zusätzlich dazu sind im 
Phasenraum Konturlinien bei ausgewählten Energien eingezeichnet."""

import functools                            # Importbefehle
import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import odeint          # Paket zum Lösen der DGL

def abl(y, t, A = 0.1, B = 0.1, omega = 1.0):
    """Rechte Seite der Bewegungsgleichung des Teilchens.
    A, B und omega sind Parameter, t ist das Zeitenarray und
    y ein Phasenraumpunkt (x, p)."""
    return np.array([y[1], -4*y[0]**3 + 2*y[0] - (A+B*np.sin(omega*t))])
    
def V(x, A):
    """Potential zum Zeitpunkt t = 0 in Abhängigkeit vom Ort x und dem
    Parameter A"""
    return x**4 - x**2 + A*x

def stroboskop(y_t, punkte, strob):
    """Zeichnet den stroboskopischen Plot der Trajektorie. Benutzt wird
    dazu das berechnete y_t-Array, aus dem die Werte nach je n Perioden
    aussortiert werden."""
    x_slice = y_t[:, 0]                     # Slice für die 1. Spalte
    p_slice = y_t[:, 1]                     # Slice für die 2. Spalte
    # in strob.plot wird der jeweils punkte-te Wert aus dem geslictem
    # Array ausgewählt und als (nicht-verbundener) Phasenraumpunkt
    # dargestellt.
    strob.plot(x_slice[::punkte], p_slice[::punkte],
        linestyle = "none", marker = ".", markersize = 4.0)
    plt.draw()

def trajektorie(y_t, traj):
    """Zeichnet die Trajektorie eines Teilchens im gegebenen Potential.
    """
    x_slice = y_t[:, 0]                     # Slices, siehe bei strob.
    p_slice = y_t[:, 1]
    # Beim Plot der Trajektorie werden alle Phasenraumpunkte gezeichnet
    # und verbunden (kontinuierliche Trajektorie)
    traj.plot(x_slice, p_slice, linewidth = 0.3, alpha = 0.5)
    plt.draw()
    
def onclick(event, abl, t, A, B, omega, traj, strob, punkte):
    """Onclick-Funktion, prüft Fenstermodus und übernimmt bei passendem
    Modus (kein Zoom, in Achsen) die Klickkoordinaten als neue Anfangs-
    werte in der Lösung der DGL. Übergeben werden t als Zeiten-Array,
    die Parameter A, B und omega, die Anzahl der Punkte pro Periode
    punkte und die Subplots traj und strob."""
    mode = plt.get_current_fig_manager().toolbar.mode
    if event.button == 1 and event.inaxes and mode == '':
        # Überprüfung des Fenstermodus
        x = event.xdata                     # Abfrage der Klickkoord.
        y = event.ydata
        # Eigentliche Lösung der DGL: übergeben werden die rechte Seite
        # der Funktion (abl), der Anfangswertvektor [x,y], das Zeiten-
        # Array t, sowie die Parameter A, B und omega.
        y_t = odeint(abl, [x, y], t, args=(A, B, omega))
        stroboskop(y_t, punkte, strob)      # Zeichnen der Trajektorien
        trajektorie(y_t, traj)

def main():
    """Docstring als Benutzerführung, definiert Parameter und Arrays
    und fängt Mausklicks im Plotfenster ab."""
    print __file__                          # Information zur Datei
    print __doc__                           # Docstring als Benutzer-
                                            # führung
    A = 0.1                                 # Parameter im Potential
    B = 0.1
    omega = 1.0
    
    perioden = 200                          # Anzahl der Perioden, die
                                            # mit jedem Klick berechnet
                                            # werden sollen
    punkte = 100                            # Anzahl der Stützpunkte pro
                                            # Periode; gleichzeitig
                                            # Anzahl der x- und p-Punkte
                                            # für die Kontourlinien
    
    # Ausgewählte Energiewerte für die Kontourlinien
    E_n = [-0.3, -0.2, -0.1, 0.0, 0.07, 0.2, 0.5, 1.0, 1.5]
    # Zeiten-Array für "perioden" Perioden mit je "punkte" Stützpunkten
    t = np.linspace(0.0, 2*perioden*np.pi / omega, num=perioden*punkte)
    
    # Legt ein meshgrid zum Zeichnen der Höhenlinien an (2D-Plot)
    # Zeichnet "Höhenlinien" des Potentials
    x_array = np.linspace(-1.5, 1.5, punkte)
    p_array = np.linspace(-2.0, 2.0, punkte)
    x_2D, p_2D = np.meshgrid(x_array, p_array)
    # Hamiltonian für B = 0.0
    H = p_2D**2/2 + x_2D**4 - x_2D**2 + x_2D*A
    
    fig = plt.figure(0, figsize=(14, 10))   # Neues Plotfenster (groß)
    
    traj = fig.add_subplot(121)             # Subplots für Trajektorien
    strob = fig.add_subplot(122)
    
    traj.set_title(u"Trajektorie für B = " + str(B))
    traj.set_xlabel("$x$")
    traj.set_ylabel("$p$")
    traj.axis([-1.5, 1.5, -2.0, 2.0])       # Plotbereich einschränken
    tr = traj.contour(x_2D, p_2D, H, E_n)   # Kontour mit Beschriftung
    plt.clabel(tr, inline = 1, fontsize = 10)
    
    strob.set_title("Stroboskopische Trajektorie")
    strob.set_xlabel("$x$")
    strob.set_ylabel("$p$")
    strob.axis([-1.5, 1.5, -2.0, 2.0])      # Plotbereich einschränken
    st = strob.contour(x_2D, p_2D, H, E_n)  # Kontour mit Beschriftung
    plt.clabel(st, inline = 1, fontsize = 10)
    
    # Klickfunktion, übergibt Parameter und Arrays an die onclick-
    # Funktion. Plt.connect fngt Mausklicks ab und leitet das Event an
    # onclick(event) um.
    klick_funktion = functools.partial(onclick, abl=abl, t=t, A=A, B=B, 
        omega=omega, traj=traj, strob=strob, punkte=punkte)
    plt.connect('button_press_event', klick_funktion)
    plt.show()
    
if __name__ == "__main__":
    main()

#       Beobachtungen:
# 
# a.    Man erwartet geschlossene Trajektorien, da der Hamiltonian 
#       zeitlich konstant ist und das Potential für \pm \infty nach 
#       \infty geht. Die Trajektorien folgen den Niveaulinien.
#
# b.    Im Ortsraum finden periodische Bewegungen statt, wobei sich das
#       Teilchen immer wieder durch die gleichen Punkte im Potential
#       bewegt. 
#
# c.    Das Teilchen bewegt sich annähernd auf den Niveaulinien, die
#       Bewegung ist allerdings etwas gestört und weicht von den
#       Kontourlinien leicht ab. In der tieferen Mulde (links) bilden
#       sich C-förmige Trajektorien, besonders deutlich ist das im
#       stroboskopischen Plot zu erkennen.
#
# d.    x(0) =  0.666
#       p(0) = -0.036
