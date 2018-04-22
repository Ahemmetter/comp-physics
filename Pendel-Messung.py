#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from matplotlib import pyplot as plt
import numpy as np
"""Auswertung von Pendelmessung
"""

table = np.loadtxt("Pendel-Messung.dat")
np.t = table[:]

def statistik (j):
    """Statistikfunktionen zusammengefasst
    """
    global mw, std, var
    mw = np.mean(j)
    var =  np.var(j)
    std = np.std(j)/np.sqrt(len(j))

statistik(np.t)

print "Mittelwert: {}, Varianz: {}, Standardabw. des Mittw.: {}".format (mw, var, std)
#print "Varianz: ", var
#print "Standardabweichung des Mittelwertes: ", std

np.bw=[]
np.am=[]
np.same=[]
for i in range (len(np.t)):
        np.bw.append(np.t[i])
        np.am.append (np.mean (np.bw))
        np.same.append(np.std(np.bw)/np.sqrt(len(np.bw)))
        mw = np.mean (np.bw)
        var = np.var (np.bw)
        std = np.std(np.bw)/np.sqrt(len(np.bw))
        print "MW: {}, Var: {}, SA. MW.: {}".format (mw, var, std)



# Intervalle
int = np.sqrt(len(np.t))

# Obere Fehler
# np.of=np.bw+np.same
# np.uf=np.bw+(np.same)
# Der Versuch hier war Listen mit den oberen und unteren Fehlern zu
# erzeugen und diese im gleichen Bild anzeigen zu lassen.


fig = plt.figure()
fig.suptitle(u"Statistikplots")

plt.subplot(221)        
plt.plot(np.am)
plt.title ("Mittelwerte")

#pl2 = plt.subplots(221,sharex=True)
#plt.plot(np.of)

plt.subplot(222)
plt.plot(np.t)
plt.title("Messwerte")

plt.subplot(223)
plt.hist(np.t, int )
plt.ylabel(u"Häufigkeit", va='bottom')

plt.subplot(224)
plt.hist(np.t, int, normed=True)
plt.ylabel(u"relative Häufigkeit")

plt.show()
