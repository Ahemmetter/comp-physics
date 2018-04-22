import numpy as np
from matplotlib import pyplot as plt
from quantenmechanik import (diskretisierung, diagonalisierung, plot_eigenfunktionen)

def V(x, A):
	return x**4 - x**2 - A*x

def wellenpaket(x, x0, dx, hbar, p0):
    vorfaktor = 1/((2*np.pi*dx**2)**0.25)
    phin = np.e**((-(x-x0)**2)/(4*dx**2))*np.e**(complex(0,1)/hbar*p0*x)
    return vorfaktor*phin

def start(event):
    mode = plt.get_current_fig_manager().toolbar.mode
    if event.button == 1 and event.inaxes and mode == "":
        x0 = event.xdata
        ew, ef, cn, phi_tilde, x_i = koeff(V, A, hbar, orte, xmin, xmax,
            wellenpaket, x0, dx, p0)
        eew = H_ew(ew, cn)
        animation(ax, ew, ef, cn, x_i, V, A, eew, phi_tilde, t, hbar, k)

def koeff(V, A, hbar, N, xmin, xmax, wellenpaket, x0, dx, p0):
	
	x_i = diskretisierung(xmin, xmax, N)
	phi_0 = wellenpaket(x_i, x0, dx, hbar, p0)
	
	ew, ef = diagonalisierung(hbar, x_i, V(x_i, A))
	c = np.abs(x_i[0]-x_i[1])*np.dot(np.conjugate(np.transpose(ef)),
        phi_0)
	
	phi_tilde = np.dot(ef, c)
	#dp = (np.abs(x_i[0]-x_i[1])*np.sum(np.abs(phi0-phi_tilde)**2))**0.5
	return ew, ef, c, phi_tilde, x_i

def H_ew(ew, cn):
	return np.dot(np.abs(cn)**2, ew)

def entw(ew, ef, c_n, t, hbar):
	return np.dot(ef, cn*np.e**((complex(0,-1)*ew*t/hbar)))
	
def ef_plot(ax, ew, ef, x, V, A):
	V_aktuell = V(x,A)
	plot_eigenfunktionen(ax, ew, ef, x, V_aktuell, width=1.5, 
        betragsquadrat=True, alpha=0.5,
        title = "asymmetrische Doppelmulde, Wellenpaket mit Zeitentwicklung")
	
def animation(ax, ew, ef, cn, x, V, A, eew, phi_tilde, t, hbar, k):
	plt.axes(ax)
	plt.cla()
	ef_plot(ax, ew, ef, x, V, A)
	plt.draw()
	paket = plt.plot(x, np.abs(phi_tilde) ** 2) #achtung
	for t_i in t:
		phi_t = entw(ew, ef, cn, t_i, hbar)
		plt.setp(paket[0], ydata = eew + k * np.abs(phi_t)**2)
		plt.draw()


def main():
    print __file__ 
    print __doc__
    
    p0 = 0.0
    A = 0.05
    hbar = 0.07
    xmin = -2.0
    xmax = 2.0
    tmax = 10.0
    zeiten = 201
    dx = 0.1
    orte = 1000

    t = np.linspace(0, tmax, zeiten)
    k = 0.01
    
    
    
    ew0, ef0, c_n0, phi_s0, x_i0 = koeff(V, A, hbar, orte, xmin, xmax, wellenpaket, 0.0, dx, p0)
    fig = plt.figure(0, figsize=(14,10))
    ax = fig.add_subplot(111)
    ef_plot(ax, ew0, ef0, x_i0, V, A)
    plt.connect("button_press_event", start)
    plt.show()

if __name__ == "__main__":
    main()

