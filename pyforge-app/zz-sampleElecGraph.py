#import viewTreePlot as vtp
import pydot
from anytree import Node, RenderTree, find_by_attr
from anytree.exporter import DotExporter
from anytree.importer import DictImporter
importer = DictImporter()
import clipboard
#import pygraphviz as pgv

#'MDP','H1A','H1B','TX1','TX2','L1A','L1B','L2A','L2B'

#lighting1={'2':235, '4':375}
#lighting2={'2':475, '4':1005}

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)

#yo = Node('yo', parent='test')

print(udo)
print(joe)
print()

#finds node in 
n=find_by_attr(udo, 'Joes')
if not n:
	print('Cant find node')
print(type(n))
print(n)

joe.children=[Node('child')]

for pre, fill, node in RenderTree(udo):
	#print(node)
	print("%s%s" % (pre, node.name))
	
# graphviz
filename='viztree.txt'
DotExporter(udo).to_dotfile(filename)
#dot tree.dot -T png -o tree.png

file = open(filename)
text = file.read()
	
if text:
	clipboard.set(text)
	print(f'({filename} GraphVix Copied to clipboard and txt file created)')
	print(text)
else:
	print('No input text found.')
pass




data = {'dinner':
            {'chicken':'good',
             'beef':'average',
             'vegetarian':{
                   'tofu':'good',
                   'salad':{
                            'caeser':'bad',
                            'italian':'average'}
                   },
             'pork':'bad'}
        }

data2 = {
     'name': 'root',
     'children': [{'a': 'sub0',
                   'children': [{'a': 'sub0A', 'b': 'foo'}, {'a': 'sub0B'}]},
                  {'a': 'sub1'}]}


def importFromDict(data):
	root = importer.import_(data)
	r=RenderTree(root)
	print(r)
	pass
print()
print(data2)
print()

importFromDict(data2)

n1=Node('')
print(n1)




