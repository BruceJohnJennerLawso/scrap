## nodeviz.py ##################################################################
## playing around with visually displaying graphs of ###########################
## connections between nodes ###################################################
################################################################################
import pygraphviz as pgv
from pygraphviz import *
## installed via apt
import random


def getAboveAndBelow(nodeNumber, nodeList):
	above = nodeNumber +1 
	below = nodeNumber -1
	while(above not in nodeList):
		above -= len(nodeList)
	while(below not in nodeList):
		below += len(nodeList)
	return above, below
		

if(__name__ == "__main__"):
	G=pgv.AGraph()
	ndlist = range(21)
	for node in ndlist:
		G.add_node(node)
		label = str(node)
		G.get_node(node).attr['label'] = label
		above, below = getAboveAndBelow(node, ndlist)
		G.add_edge(str(node),above)
		G.add_edge(str(node),above + int(3*random.random()))
	G.layout()
	G.draw('nodesviz_example.png', format='png')
