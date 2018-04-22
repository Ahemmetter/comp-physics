#!/usr/bin/python       #Header
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 21:20:19 2015

@author: David
"""

import numpy as np
from matplotlib import pyplot as plt


def modp(p):
    return (p+np.pi) % (2*np.pi)-np.pi

def Iteration(t0, p0, n=1000):
    for i in np.arange(0,n):
        if i==0:
            t=[t0]
            p=[p0]
        t.append((t[-1]+p[-1]) % (2*np.pi))
        p.append(modp(p[-1]+K*np.sin(t[-1])))
    return t,p

def MouseClick(event):
    if plt.get_current_fig_manager().toolbar.mode=="":
            x, y=Iteration(event.xdata, event.ydata)
            plt.plot(x, y)
            plt.draw()

if __name__=="__main__":
    K=0.5

    plt.figure(0)
    plt.subplot(111, autoscale_on=False)
    plt.title("Phase Space Diagram")
    plt.axis([0, 2*np.pi, -np.pi, np.pi])
    plt.xlabel(r"$\theta$")
    plt.ylabel(r"$p_n$")
    plt.xticks(np.arange(0,2*np.pi+0.1,np.pi/2), (r"$0$", r"$\pi/2$", r"$\pi$",
               r"$3/2\pi$", r"$2\pi$"))
    plt.yticks(np.arange(-np.pi,np.pi+0.1,np.pi/2),(r"-$\pi$", r"-$\pi/2$",
               r"$0$",r"$\pi/2$", r"$\pi$"))               
    plt.connect('button_press_event', MouseClick)
    plt.show()
