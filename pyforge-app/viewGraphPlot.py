import pydot
import tempfile
import Image
import clipboard
import webbrowser
from anytree import Node, RenderTree, find_by_attr
from anytree.exporter import DotExporter
from anytree.importer import DictImporter
importer = DictImporter()

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)


#Send dictionary value
def createAndWriteGraph(data=udo):
	print('print graph')
	#print(RenderTree(data))
	for pre, fill, node in RenderTree(data):
		print("%s%s" % (pre, node.name))	
	#visit(data)	
	filename='vizgraph.txt'
	#saves text of graph
	#graph.write(filename) 
	DotExporter(data).to_dotfile(filename)
	
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

if __name__ == '__main__':
	createAndWriteGraph()
else:
	print('viewGraphPlot Imported')
