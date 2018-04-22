#-*- coding: utf-8 -*-

"""Programm plottet Ellipsenbahnen der Erde und des Halley'schen Kometen
mit python-visual."""

import visual as vi #pyhton-visual enthält bereits die Pakete math und
#numpy, müssen also nicht mehr geladen werden.

def a(r1, r2):
	"""Funktion zur Berechnung der Beschleunigung eines Körpers (Vektor)
	"""
	return -(4*vi.pi**2 * (r2-r1) / (vi.mag(r2-r1)**3))

#Sonne:
sun = vi.sphere(material=vi.materials.emissive, color=vi.color.yellow, \
radius=0.5)
sp = vi.vector(0,0,0) #Koordinatenursprung

#Erde: (eine Einheit = 1AU)
e1 = 0.017 #Exzentrität der Erdumlaufbahn
aphel1 = (e1+1) * 1
ep = vi.vector(aphel1, 0, 0) #Position der Erde
earth = vi.sphere(pos=ep, material=vi.materials.earth, radius = 0.2)
earth.trail = vi.curve(color=vi.color.green) #Trajektorie der Erde
ve = vi.sqrt(4*vi.pi**2 * (2/vi.mag(ep) - 1/1))*vi.vector(0,0,-1)

#Halley'scher Komet:
e2 = 0.97 #verglichen mit der Erde stark elliptisch
aphel2 = (e2+1)*17.94
cp = vi.vector(aphel2, 0, 0)
comet = vi.sphere(pos=cp, color=vi.color.white, radius=0.1)
comet.trail = vi.curve(color=comet.color) #Trajektorie des Kometen
vc = vi.sqrt(4 * vi.pi ** 2 * (2 / vi.mag(cp) - 1 / 17.94)) * \
vi.vector(0, 0, -1)

vi.scene.autoscale = False

dt = 0.001 #kleine Zeitabstände
i = 0
cometTrail = True
earthTrail = True
while True:
	i += dt
	vi.rate(100) #Wartezeit für Animation in VPython

	ve = ve+a(sp, ep) * dt
	ep = ep+ve*dt
	earth.pos = ep

	vc = vc+a(sp, cp) * dt
	cp = cp+vc * dt
	comet.pos = cp

	if cometTrail:
		"""Plottet Bahnkurve des Kometen"""
		comet.trail.append(comet.pos)

	if earthTrail:
		"""Plottet Bahnkurve der Erde"""
		earth.trail.append(earth.pos)

	if vi.mag(vc) < 0.2 and i > 5 and cp.z < 0:
		cometTrail = False
