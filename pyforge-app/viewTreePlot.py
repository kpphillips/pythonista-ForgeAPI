import pydot
import tempfile
import Image
import clipboard
import webbrowser
from anytree import Node, RenderTree, find_by_attr
from anytree.exporter import DotExporter
from anytree.importer import DictImporter
importer = DictImporter()

sample = {'dinner':
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


graph = pydot.Dot(graph_type='graph')

def draw(parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)

def visit(node, parent=None):
    for k,v in node.items():
        if isinstance(v, dict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if parent:
                draw(parent, k)
            visit(v, k)
        else:
            draw(parent, k)
            # drawing the label using a distinct name
            print(k)
            print(type(v))
            if isinstance(v, str):
            	draw(k, k+'_'+v)

#Send dictionary value
def createAndWriteGraph(data=sample):
	print('print graph')
	#print(RenderTree(data))
	for pre, fill, node in RenderTree(data):
		print("%s%s" % (pre, node))	
	visit(data)	
	filename='vizgraph.txt'
	#saves text of graph
	graph.write(filename) 
	
	file = open(filename)
	text = file.read()
	
	if text:
		clipboard.set(text)
		print(f'({filename}GraphVix Copied to clipboard and txt file created)')
		url = 'http://www.webgraphviz.com/'
		# Open URL in a new tab, if a browser window is already open.		
		webbrowser.open_new_tab(url)
		print('Added Tab for Graphviz website')
	else:
		print('No input text found.')
	pass
	

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)

def createAndWriteTree(data=udo):
	#print('print tree')
	print(RenderTree(data))
	for pre, fill, node in RenderTree(data):
		print('tree loop')
		print("%s%s" % (pre, node))	
	filename='viztree.txt'
	#saves text of tree	
	DotExporter(udo).to_dotfile(filename)
	#dot tree.dot -T png -o tree.png
	
	file = open(filename)
	text = file.read()
	
	if text:
		clipboard.set(text)
		print(f'({filename}GraphVix Copied to clipboard and txt file created)')
		url = 'http://www.webgraphviz.com/'
		# Open URL in a new tab, if a browser window is already open.		
		webbrowser.open_new_tab(url)
		print('Added Tab for Graphviz website')
	else:
		print('No input text found.')
	pass

def importFromDict(data):
	root = importer.import_(data)
	print(RenderTree(root))
	for pre, fill, node in RenderTree(root):
		print("%s%s" % (pre, node.name))
	pass

if __name__ == '__main__':
	#createAndWriteGraph()
	createAndWriteTree()
else:
	print('viewTreePlot Imported')

