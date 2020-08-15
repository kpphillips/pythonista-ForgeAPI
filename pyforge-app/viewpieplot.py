# coding: utf-8
'''
Plots pie chart
'''

import matplotlib.pyplot as plt
import random

def piePlot(labels,sizes):
	# The slices will be ordered and plotted counter-clockwise.
	#explode = (0, 0, 0, 0) # add point value to explode
	#plt.pie(sizes,labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=90)
	#colors=[]
	#for i in sizes:
		#colors.append(generate_color())
	
	#labelsConcat=[]
	#for f, b in zip(labels, sizes):
		#l=f'{f} {b}'
		#labelsConcat.append(l)
	
	plt.pie(sizes,labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
	# Set aspect ratio to be equal so that pie is drawn as a circle.
	plt.axis('equal')
	plt.show()
	plt.clf()
	
def generate_color():
    color = '#{:02x}{:02x}{:02x}'.format(*map(lambda x: random.randint(0, 255), range(3)))
    return color

def piePlotSample():
	#sample data
	labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'	
	sizes = [2, 1, 2, 1]
	piePlot(labels,sizes)
	plt.clf()
	pass
	
def piePlotSample2():
	#sample data
	labels = 'Frogs', 'Hogs', 'Dogs'
	sizes = [8, 1, 8]
	piePlot(labels,sizes)
	plt.clf()
	pass	
	
#piePlotSample()
#piePlotSample2()



