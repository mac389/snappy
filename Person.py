import numpy as np

from random import random, choice

class Person(object):
	def __init__(self,id,decay=0.01):
		#Start with a single initial preference
		self.parameters = { 'id':id, 'initial-preference':random(),'acceptance':0.8}
		self.parameters['attitude'] =  self.parameters['initial-preference'] #Attitude begins with initial preference
	'''
	def __repr__(self):
		return 'Person(%s)'%(' '.join(sorted(self.parameters.items())))
	'''
	def __str__(self):
		return str(self.parameters['id'])
	'''
	def step(self,world):
		#Loop through FIRST neighbors and aggregate their preferences
		neighbors = world[self]
		consensus = np.average([neighbor.parameters['attitude'] for neighbor in neighbors]+[self.parameters['attitude']])
		self.parameters['attitude'] = self.parameters['acceptance']*(consensus-self.parameters['initial-preference'])+self.parameters['initial-preference']
	'''
	def _roulette_choice(self,world,inverse=False):
		wheel = world[self]
		for i in range(len(world[self])):
			for neighbor in world[self]:
				if not inverse:
					cutoff = 1+int(world[self][neighbor]['weight']*10)
				else: 
					cutoff = 1 + int((1-world[self][neighbor]['weight'])*10)	
				wheel.extend([wheel[i]]*cutoff)

	def interact(self,world):
		partner = choice(world.nodes())
		consensus = np.average(self.parameters['attitude'] + partner.parameters['attitude'])

		#update beliefs	
		self.parameters['attitude'] = self.parameters['acceptance']*(consensus-self.parameters['initial-preference'])+self.parameters['initial-preference']
		world.add_edge(self,partner,weight=(1-self.parameters['attitude']-partner.parameters['attitude']))

