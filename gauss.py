# -*- coding: utf-8 -*- 

from random import randint
import random

def run():
	X = []
	Y = []

	for i in range(0,1000):
		#cylinder
		summe = 0
		for k in range(0,12):
			r = random.uniform(0,1)
			summe = summe+r
			#print summe
		X.append(1+0.01*(summe-6))

	for i in range(0,1000):
		#stick
		summe = 0
		for k in range(0,12):
			r = random.uniform(0,1)
			summe = summe+r
		Y.append(0.99+0.01*(summe-6))
	c = 1000
	d = 1000
	k = 0
	for i in range(0,1000):

		m = randint(0,c-1)
		n = randint(0,d-1)

		if X[m] - Y[n] >= 0:
			k = k+1

		X.pop(m)
		Y.pop(n)

		c = c-1
		d = d-1

	f = k/1000.0
	print (1-f)*100

for i in range(0,10):
	run()
