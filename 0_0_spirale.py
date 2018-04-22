"""Zeichnet eine Spirale nach Linksklick mit Zentrum im ausgewaehlten Punkt."""

import numpy as np
from matplotlib import pyplot as plt               # Graphikbefehle


def spirale(x0=0.0, y0=0.0):
    """Berechnet eine Spirale mit Zentrum (x0,y0)."""
    anz = 5                                        # Zahl der Windungen
    t = np.linspace(0, anz, 1000)                  # Parameterisierungsvariable
    r = 0.5**t                                     # Radius
    phi = 2.0 * np.pi * t                          # Winkel

    x = r*np.cos(phi) + x0                         # x-Koordinate
    y = r*np.sin(phi) + y0                         # y-Koordinate

    return x, y


def neuer_punkt(event):
    """Nach Linksklick, plotte Spirale mit Zentrum im ausgewaehlten Punkt."""
    # Test, ob Klick mit linker Maustaste und im Koordinatensystem
    # erfolgt sowie ob Zoomfunktion des Plotfensters deaktiviert ist:
    mode = plt.get_current_fig_manager().toolbar.mode
    if event.button == 1 and event.inaxes and mode == '':
        x, y = spirale(event.xdata, event.ydata)   # Spirale neu berechnen, am
        plt.plot(x, y)                             # angeklickten Ort plotten
        plt.draw()                                 # und anzeigen

# Benutzerfuehrung (was soll der Benutzer machen?):
print "Mit linker Maustaste Punkt festlegen"

# Quadratischer Plotbereich, keine automatische Skalierung:
plt.subplot(111, aspect=1.0, autoscale_on=False)
plt.axis([-1, 1, -1, 1])                           # Plotbereich
plt.xlabel("x")                                    # Labels
plt.ylabel("y")                                    # definieren

x_pkt, y_pkt = spirale()                           # erste Spirale ohne Klick
plt.plot(x_pkt, y_pkt)                             # erste Spirale zeichnen

# Bei Mausklick soll die Funktion ``neuer_punkt`` aufgerufen werden:
plt.connect('button_press_event', neuer_punkt)

# Endlos-Schleife, die auf Ereignisse wartet:
plt.show()
