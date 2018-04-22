"""Zeitentwicklung von Gauss-Wellenpaketen.

Beispiel: asymmetrisches Doppelmuldenpotential $V(x)=x^4-x^2+A x$.
"""

from numpy import *
from matplotlib import pyplot as plt
import quantenmechanik as qm


def potential(x, A):
    """Potentialfunktion fuer die asymmetrische Doppelmulde mit Parameter A."""
    return x**4 - x**2 + A*x


def gausspaket(x, x0, p0, hquer, Delta_x=0.1):
    """Gausspaket um (x0, p0) mit Breite Delta_x, berechnet am Ort x.

    Weiterer Paraemter: effektives 'hquer'.
    """
    return (1.0/sqrt(sqrt(2.0*pi)*Delta_x)
            * exp(-(x - x0)**2/(4*Delta_x**2))
            * exp(1j*p0*x/hquer))


def plot_zeitentwicklung(ax, ew, ef, x, V, coeff, hquer, fak, zeiten):
    """Berechne und plotte die Zeitentwicklung eines Wellenpakets.

    Das Wellenpakets ist bestimmt durch die Entwicklungskoeffizienten 'coeff'.
    Uebergeben werden der Plotbereich 'ax', die Eigenwerte 'ew',
    die Eigenfunktionen 'ef', das Potential 'V' an den Orten 'x',
    das effektive 'hquer', der Skalierungsfaktor 'fak'
    und das Zeitarray 'zeiten'.
    """
    ax.lines = []                                 # entfernt alle Linien
    E0_qm = dot(abs(coeff)**2, ew)                # qm. Energieerwartung
    phi_t0 = dot(ef, coeff)                       # Anfangswellenpaket

    prop_coeff = abs(coeff)**2                    # Anregungswahrscheinlichkeit
    prop_coeff = prop_coeff/max(prop_coeff)       # ... normiert auf Maximum

    phi_t0_scaled = E0_qm + fak*abs(phi_t0)**2  # skaliertes Wellenpaket

    # Plot mit Transparenz proportional zur Anregungsstaerke
    qm.plot_eigenfunktionen(ax, ew, ef, x, V, width=2, fak=fak,
                            betragsquadrat=True, alpha=prop_coeff)
    # plotte initial Wellenpaket
    wellenpaket = plt.plot(x, phi_t0_scaled, linewidth=4, c='k')
    plt.draw()
    print "Energieerwartungswert des Wellenpakets:", E0_qm
    print "Zeitentwicklung laeuft ..."
    # Zeitentwicklung des Gausswellenpakets:
    for t in zeiten[1:]:
        phi = dot(ef, coeff*exp(-1j*ew*t/hquer))    # Berechnung von phi(t)
        plt.setp(wellenpaket[0],
                 ydata=E0_qm + fak*abs(phi)**2)   # plot |phi(t)|^2
        plt.draw()
    print "fertig!"
    print
    print "Linksklick startet neues Wellenpaket."


def wp_neu(event):
    """Neues Wellenpaket mit Maus festlegen und Zeitentwicklung darstellen.

    Es werden diverse globale Variablen genutzt, u.a.:
        x: Werte des Diskretisierung.
        p0: Impulsmittelwert des Gausswellenpakets
            Ortsmittelwert wurd durch Mausklick gegeben
        hquer: effektives hquer
        delta_x_gauss: Ortsbreite des Gausswellenpakets
        ew, ef: Eigenwerte und Eigenvektoren des Hamiltonoperators
    """
    if (event.button == 1 and event.inaxes and
            plt.get_current_fig_manager().toolbar.mode == ''):
        # Anfangswellenpaket
        phi0 = gausspaket(x, event.xdata, p0, hquer, Delta_x=delta_x_gauss)
        # Entwicklungskoeffizienten
        delta_x = x[1] - x[0]               # Intervall der Ortsdiskretisierung
        coeff = dot(conjugate(transpose(ef)), phi0)*delta_x
        # Rekonstruktion
        phi_t0 = dot(ef, coeff)

        print "Norm des Fehlers:", sqrt(sum(abs(phi_t0 - phi0)**2)*delta_x)
        plot_zeitentwicklung(ax, ew, ef, x, V, coeff, hquer, fak, zeiten)


def main():
    """Hauptprogramm."""
    global x, ew, ef, p0, V, hquer, zeiten, delta_x_gauss, ax, fak

    p0 = 0                                  # Impuls des WP
    A = 0.04                                # Potentialparameter
    L = 2.0                                 # x-Bereich ist [-L,L]
    N = 500                                 # Zahl der Gitterpkte
    hquer = 0.05                            # effektives hquer
    delta_x_gauss = 0.1                     # Breite Gauss
    zeiten = linspace(0.0, 4, 200)          # Zeiten f. Zeitentw.
    fak = 0.01                              # Plot-Skalierungsfak.
    Emax = 0.1                              # Maximalenergie fuer Darstellung

    x = qm.diskretisierung(-L, L, N)
    V = potential(x, A)

    ew, ef = qm.diagonalisierung(hquer, x, V)
    print "Energiedifferenz E_1 - E_0:", ew[1] - ew[0]

    ax = plt.subplot(111, autoscale_on=False)
    qm.plot_eigenfunktionen(ax, ew, ef, x, V, Emax=Emax,
                            fak=fak, betragsquadrat=True)
    plt.setp(ax, title="Zeitentwicklung im asymm. Doppelmuldenpotential")

    print __doc__
    print "Linksklick startet neues Wellenpaket."

    plt.connect('button_press_event', wp_neu)

    plt.show()


if __name__ == "__main__":
    main()