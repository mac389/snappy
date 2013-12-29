import pylab

import Person as blueprint
import Influencer as pundit
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from random import random,choice
from matplotlib.animation import ArtistAnimation

density = 0.9
g = nx.Graph()

population = {'influencers':0,'masses':10}
for i in xrange(population['masses']):
	g.add_node(blueprint.Person(i))


#----Model initialization
#Simple random graph, every pair of nodes has an equal probability of connection
for x in g.nodes():
	for y in g.nodes():
		if random() <= density:
			g.add_edge(x,y)

#----Include influencers
connections = 4 #Magic constant!
for i in xrange(population['influencers']):
	g.add_edge(choice(g.nodes()), pundit.Influencer(i))

timesteps = 100
opinion = np.zeros((timesteps,sum(population.values())))
pylab.ion()
pos = nx.spring_layout(g)
images = []
for i in range(timesteps):
	#iterate through all nodes in the network and have each of them make a step
	#Isn't it better to just pick one node randomly?
	for node in g.nodes():
		node.interact(g)

	plt.clf()
	wts=np.array([edge[2]['weight'] if 'weight' in edge[2] else 0 for edge in g.edges_iter(data=True)])
	wts = (wts-wts.min())/(wts.max()-wts.min())
	line = nx.draw_networkx(g,pos=pos,edge_color=wts, width=4,edge_cmap = plt.cm.binary)
	plt.gca().annotate('%d/%d'%(i,timesteps), xy=(.1, .1),  xycoords='axes fraction',
                horizontalalignment='center', verticalalignment='center')
	plt.colorbar()
	plt.axis('off')

	opinion[i,:] = [node.parameters['attitude'] for node in g.nodes()]

'''
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.imshow(opinion.T,aspect='auto',interpolation='nearest', vmin=0,vmax=1)
ax.set_xlabel('Timesteps')
ax.set_ylabel('Person')
plt.colorbar(cax)
'''
plt.show()