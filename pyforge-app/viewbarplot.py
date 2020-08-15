import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def plotBar(objects, data, filename):
	y_pos = np.arange(len(objects))
	plt.bar(y_pos, data, width=0.5, align='center', alpha=0.5)
	plt.xticks(y_pos, objects)
	plt.xticks(rotation='vertical')
	plt.ylabel('Mbs - Next Gen Includes Links')
	plt.title(f'{filename}')
	#plt.margins(0.2)
	plt.subplots_adjust(bottom=0.18)
	plt.show()
	plt.clf()

#sample data
'''
Sample Data format
objects = ['Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp']
data = [15,8,6,4,2,1]
filename = 'Filename'
'''
