class Influencer(object):
	def __init__(self,id):
		self.parameters = { 'id':'Inf %d'%id, 'initial-preference':1,'acceptance':0}
		self.parameters['attitude'] =  self.parameters['initial-preference'] #Attitude begins with initial preference

	def step(self,*args):
		pass

	def interact(self,*args):
		pass
		
	def __str__(self):
		return str(self.parameters['id'])
