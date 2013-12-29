#!/usr/bin/env python
import random
import pylab
from matplotlib.pyplot import pause,cm
import networkx as nx
import numpy as np
pylab.ion()

graph = nx.Graph()
node_number = 0
graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))
weights = []

def laplacian(graph):
    a=len(graph.nodes())
    sb=dict((a,i) for a,a in enumerate(graph.nodes()))
    r = np.zeros((a,a)) #So, apparently this method for making a 0 matrix exists.
    for sc,d in enumerate(graph.nodes()):
        f=0.0
        for p,dt in graph[d].items():
            s=sb[p]
            r[sc,s]= -1
            f += 1
        r[sc,sc]= f
    return r

def get_fig():
    global node_number
    node_number += 1
    graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))
    wt = random.choice(graph.nodes())
    weights.append(wt)
    graph.add_edge(node_number, random.choice(graph.nodes()),weight=wt)
    nx.draw(graph, edge_color=weights, edge_cmap = cm.binary,width=4,pos=nx.get_node_attributes(graph,'Position'))

num_plots = 6;
pylab.show()

for i in range(num_plots):
    get_fig()
    pylab.draw()
    pause(.25)
    
print(laplacian(graph))
